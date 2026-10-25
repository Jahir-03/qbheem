"""Module 2 - Classical post-processing (runs over an authenticated public channel)."""
import math
import numpy as np

QBER_THRESHOLD = 0.11   # asymptotic BB84 bound with one-way post-processing


def h2(p):
    p = min(max(p, 1e-12), 1 - 1e-12)
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


# ---- sifting --------------------------------------------------------------
def sift(alice_bits, alice_bases, bob_bits, bob_bases):
    """Publicly compare bases (never bit values); keep matching positions."""
    keep = alice_bases == bob_bases
    return alice_bits[keep], bob_bits[keep], keep


# ---- error estimation -----------------------------------------------------
def estimate_qber(a_sifted, b_sifted, sample_frac, rng):
    """Reveal a random sample, compute QBER, return the remaining (unrevealed) key."""
    n = len(a_sifted)
    m = max(1, int(n * sample_frac))
    idx = rng.permutation(n)
    s, rest = idx[:m], np.sort(idx[m:])
    qber = float(np.mean(a_sifted[s] != b_sifted[s]))
    return qber, m, a_sifted[rest], b_sifted[rest]


# ---- error correction (simplified Cascade) --------------------------------
def _parity(bits, idx):
    return int(bits[idx].sum() & 1)


def cascade(alice, bob, qber, rng, max_cleanup=6):
    """Simplified Cascade: parity checks on blocks + binary search for the bad bit.
    No back-tracking; extra cleanup passes substitute for it.
    Returns (corrected_bob, leaked_bits). Every disclosed parity counts as leakage."""
    n = len(alice)
    bob = bob.copy()
    leaked = 0
    # assume at least 1% errors: a small sample can badly underestimate a low QBER
    k = int(min(max(4, 0.73 / max(qber, 0.01)), n))

    def run_pass(block, perm):
        nonlocal leaked
        fixed = 0
        for s in range(0, n, block):
            idx = perm[s:s + block]
            leaked += 1
            if _parity(alice, idx) != _parity(bob, idx):
                while len(idx) > 1:                  # binary search for the error
                    half = idx[:len(idx) // 2]
                    leaked += 1
                    idx = half if _parity(alice, half) != _parity(bob, half) else idx[len(idx) // 2:]
                bob[idx[0]] ^= 1
                fixed += 1
        return fixed

    ident = np.arange(n)
    run_pass(k, ident)
    for p in (1, 2, 3):
        run_pass(min(k * 2 ** p, n), rng.permutation(n))
    clean = 0
    for _ in range(max_cleanup):
        fixed = run_pass(k, rng.permutation(n))
        clean = clean + 1 if fixed == 0 else 0
        if clean == 2:
            break
    return bob, leaked


def verification_tag(bits, seed_bytes=b"verify"):
    """64-bit tag to confirm both sides hold identical keys (counted as 64 leaked bits)."""
    import hashlib
    return hashlib.sha256(seed_bytes + np.packbits(bits).tobytes()).digest()[:8]


# ---- privacy amplification ------------------------------------------------
def secure_key_length(n, qber, leaked, n_sample, eps_pe=1e-6, eps_sec=1e-9):
    """Finite-key style estimate: l = n(1 - h2(q_upper)) - leak - 2 log2(1/eps_sec).
    q_upper adds a Hoeffding margin for having estimated QBER from a finite sample."""
    margin = math.sqrt(math.log(1 / eps_pe) / (2 * n_sample))
    q = min(qber + margin, 0.5)
    l = n * (1 - h2(q)) - leaked - 2 * math.log2(1 / eps_sec)
    return max(0, int(math.floor(l)))


def toeplitz_hash(bits, out_len, seed_bits):
    """Universal (Toeplitz) hashing over GF(2): out = T @ bits mod 2.
    seed_bits (len n+out_len-1) is public but must be chosen after the quantum phase."""
    n = len(bits)
    i = np.arange(out_len)[:, None] - np.arange(n)[None, :] + (n - 1)
    T = seed_bits[i].astype(np.int64)
    return (T @ bits.astype(np.int64) % 2).astype(np.uint8)
