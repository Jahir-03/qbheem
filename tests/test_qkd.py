import numpy as np, pytest
from qkd import quantum as q, postprocessing as pp
from qkd.protocol import SessionConfig, run_session
from qkd.application import make_transaction, encrypt_transaction, decrypt_transaction
from qkd import rsa_baseline


def test_clean_channel_has_zero_errors():
    rng = np.random.default_rng(0)
    r = q.transmit(4000, rng)
    a, b, _ = pp.sift(r.alice_bits, r.alice_bases, r.bob_bits, r.bob_bases)
    assert 0.45 < len(a) / 4000 < 0.55 and (a == b).all()


def test_intercept_resend_gives_25_percent_qber():
    rng = np.random.default_rng(1)
    r = q.transmit(40000, rng, eve_active=True)
    a, b, _ = pp.sift(r.alice_bits, r.alice_bases, r.bob_bits, r.bob_bases)
    assert abs(np.mean(a != b) - 0.25) < 0.015


def test_partial_intercept_scales_linearly():
    rng = np.random.default_rng(2)
    r = q.transmit(40000, rng, eve_active=True, eve_fraction=0.4)
    a, b, _ = pp.sift(r.alice_bits, r.alice_bases, r.bob_bits, r.bob_bases)
    assert abs(np.mean(a != b) - 0.10) < 0.015


def test_cascade_corrects_noise():
    rng = np.random.default_rng(3)
    a = rng.integers(0, 2, 5000, dtype=np.uint8)
    b = a.copy(); b[rng.random(5000) < 0.03] ^= 1
    fixed, leaked = pp.cascade(a, b, 0.03, rng)
    assert (fixed == a).all() and leaked < 5000 * 0.5


def test_privacy_amplification_is_linear_and_deterministic():
    rng = np.random.default_rng(4)
    x = rng.integers(0, 2, 1000, dtype=np.uint8); y = rng.integers(0, 2, 1000, dtype=np.uint8)
    seed = rng.integers(0, 2, 1000 + 255, dtype=np.uint8)
    h = lambda v: pp.toeplitz_hash(v, 256, seed)
    assert (h(x) == h(x)).all() and (h(x ^ y) == h(x) ^ h(y)).all()


@pytest.mark.parametrize("backend", ["numpy", "qiskit"])
def test_end_to_end_success_then_aes(backend):
    r = run_session(SessionConfig(n_qubits=8192, noise=0.01, seed=7, backend=backend))
    assert r.success and len(r.alice_key) == 32
    tx = make_transaction()
    assert decrypt_transaction(r.bob_key, encrypt_transaction(r.alice_key, tx)) == tx


@pytest.mark.parametrize("backend", ["numpy", "qiskit"])
def test_eve_is_detected_and_no_key_released(backend):
    r = run_session(SessionConfig(n_qubits=8192, noise=0.01, eve_active=True, seed=8, backend=backend))
    assert r.aborted and r.alice_key is None and r.qber > 0.11


def test_tampered_ciphertext_rejected():
    key = bytes(32); pkt = encrypt_transaction(key, make_transaction())
    pkt["ciphertext"] = ("00" if pkt["ciphertext"][:2] != "00" else "11") + pkt["ciphertext"][2:]
    with pytest.raises(ValueError):
        decrypt_transaction(key, pkt)


def test_rsa_mitm_is_silent():
    r = rsa_baseline.rsa_handshake(mitm=True, bits=1024)
    assert r["keys_match"] and r["eve_knows_key"] and not r["anyone_detected_eve"]


def test_toy_rsa_falls():
    assert rsa_baseline.harvest_now_decrypt_later()["recovered"]
