"""Runs the full BB84 session: quantum -> sift -> QBER check -> EC -> PA."""
from dataclasses import dataclass, field
import numpy as np
from . import quantum as q
from . import postprocessing as pp

KEY_BITS = 256


@dataclass
class SessionConfig:
    n_qubits: int = 16384
    eve_active: bool = False
    eve_fraction: float = 1.0
    noise: float = 0.0
    sample_frac: float = 0.2
    qber_threshold: float = pp.QBER_THRESHOLD
    backend: str = "numpy"          # "numpy" or "qiskit"
    seed: int = None


@dataclass
class SessionResult:
    config: SessionConfig
    n_raw: int = 0
    n_sifted: int = 0
    n_sample: int = 0
    qber: float = 0.0
    n_after_pe: int = 0
    leaked_ec: int = 0
    secure_len: int = 0
    aborted: bool = False
    reason: str = ""
    alice_key: bytes = None
    bob_key: bytes = None
    eve_sifted_accuracy: float = None   # how much of the sifted key Eve guessed right
    log: list = field(default_factory=list)

    @property
    def success(self):
        return not self.aborted and self.alice_key is not None and self.alice_key == self.bob_key


def run_session(cfg: SessionConfig) -> SessionResult:
    rng = np.random.default_rng(cfg.seed)
    r = SessionResult(config=cfg, n_raw=cfg.n_qubits)
    log = r.log.append

    if cfg.backend == "qiskit":
        from .quantum_qiskit import transmit_qiskit as tx
    else:
        tx = q.transmit
    run = tx(cfg.n_qubits, rng, cfg.eve_active, cfg.eve_fraction, cfg.noise)
    log(f"Alice sent {cfg.n_qubits} qubits ({cfg.backend} backend)" + (" (Eve is tapping the line)" if cfg.eve_active else ""))

    a, b, keep = pp.sift(run.alice_bits, run.alice_bases, run.bob_bits, run.bob_bases)
    r.n_sifted = len(a)
    log(f"Sifting: bases matched on {r.n_sifted} positions")
    if cfg.eve_active:   # analysis only - Eve's guess for each sifted bit
        guess = np.where(run.eve_mask, run.eve_bits, rng.integers(0, 2, cfg.n_qubits))[keep]
        r.eve_sifted_accuracy = float(np.mean(guess == a))

    qber, m, a, b = pp.estimate_qber(a, b, cfg.sample_frac, rng)
    r.qber, r.n_sample, r.n_after_pe = qber, m, len(a)
    log(f"Error estimation: {m} bits revealed, QBER = {qber:.2%}")

    if qber > cfg.qber_threshold:
        r.aborted = True
        r.reason = f"QBER {qber:.2%} exceeds {cfg.qber_threshold:.0%} threshold - eavesdropper or excessive noise"
        log("ABORT: " + r.reason)
        return r

    b_fixed, leaked = pp.cascade(a, b, qber, rng)
    leaked += 64
    for _ in range(3):      # tags differ -> run more parity passes (each tag costs 64 bits)
        if pp.verification_tag(a) == pp.verification_tag(b_fixed):
            break
        b_fixed, more = pp.cascade(a, b_fixed, max(qber, 0.02), rng)
        leaked += more + 64
    r.leaked_ec = leaked
    if pp.verification_tag(a) != pp.verification_tag(b_fixed):
        r.aborted, r.reason = True, "Error-correction verification failed"
        log("ABORT: " + r.reason)
        return r
    log(f"Error correction: keys agree, {leaked} bits disclosed")

    r.secure_len = pp.secure_key_length(len(a), qber, leaked, m)
    if r.secure_len < KEY_BITS:
        r.aborted = True
        r.reason = f"Secure key length {r.secure_len} < {KEY_BITS} after leakage/finite-size bounds"
        log("ABORT: " + r.reason)
        return r

    seed = rng.integers(0, 2, len(a) + KEY_BITS - 1, dtype=np.uint8)   # public hash seed
    r.alice_key = np.packbits(pp.toeplitz_hash(a, KEY_BITS, seed)).tobytes()
    r.bob_key = np.packbits(pp.toeplitz_hash(b_fixed, KEY_BITS, seed)).tobytes()
    log(f"Privacy amplification: {r.secure_len} secure bits available, hashed to a {KEY_BITS}-bit AES key")
    return r
