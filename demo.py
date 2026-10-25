"""Command-line walkthrough: honest exchange, then the same exchange with Eve tapping the line.
   python demo.py [--qiskit]"""
import sys
from qkd.protocol import SessionConfig, run_session
from qkd.application import make_transaction, encrypt_transaction, decrypt_transaction
from qkd import rsa_baseline

backend = "qiskit" if "--qiskit" in sys.argv else "numpy"


def scenario(title, eve):
    print(f"\n=== {title} ===")
    r = run_session(SessionConfig(n_qubits=16384, noise=0.01, eve_active=eve, backend=backend, seed=42))
    for line in r.log:
        print("  ", line)
    if r.success:
        tx = make_transaction()
        pkt = encrypt_transaction(r.alice_key, tx)
        print("   Bank A sends   :", pkt["ciphertext"][:48] + "...")
        print("   Bank B decrypts:", decrypt_transaction(r.bob_key, pkt))
    else:
        print("   No transaction key released - transfer not sent.")


scenario("Honest line", eve=False)
scenario("Eve taps the line (intercept-resend)", eve=True)
print("\n=== RSA baseline with a man in the middle ===")
print("  ", rsa_baseline.rsa_handshake(mitm=True))
print("   toy harvest-now-decrypt-later:", rsa_baseline.harvest_now_decrypt_later())
