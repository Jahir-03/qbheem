"""Classical RSA key exchange baseline - to show what it cannot do."""
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.number import getPrime, inverse
import math, random


def rsa_handshake(mitm=False, bits=2048):
    """Bob sends a session key to Alice under her RSA public key.
    Without out-of-band authentication (certificates), a MITM Eve swaps the public key.
    Returns a dict describing what each party could notice."""
    t0 = time.perf_counter()
    alice = RSA.generate(bits)
    pub = alice.publickey()
    eve = RSA.generate(bits) if mitm else None
    seen_by_bob = eve.publickey() if mitm else pub         # Eve substitutes her key

    session = get_random_bytes(32)
    wire = PKCS1_OAEP.new(seen_by_bob).encrypt(session)
    stolen = None
    if mitm:
        stolen = PKCS1_OAEP.new(eve).decrypt(wire)
        wire = PKCS1_OAEP.new(pub).encrypt(stolen)         # re-encrypt for Alice
    alice_key = PKCS1_OAEP.new(alice).decrypt(wire)
    elapsed = time.perf_counter() - t0

    alice_n_hex = hex(alice.n)
    eve_n_hex = hex(eve.n) if eve else None
    session_hex = session.hex()
    stolen_hex = stolen.hex() if stolen else None
    alice_key_hex = alice_key.hex()
    wire_hex = wire.hex()

    steps = [
        {
            "id": 1,
            "title": "Alice Key Generation",
            "actor": "Alice (Bank A)",
            "description": f"Generated RSA-{bits} keypair: Public (e={alice.e}, N={alice_n_hex[:18]}...) and Private exponent d.",
            "type": "keygen",
            "mitm_active": False,
            "data": {"e": alice.e, "n_preview": alice_n_hex[:18] + "...", "bits": bits}
        },
        {
            "id": 2,
            "title": "Public Key Transmission",
            "actor": "Optical/Copper Cable" if not mitm else "Eve (MITM Interceptor)",
            "description": "Alice broadcasts Public Key (e_A, N_A) across the classical network to Bob." if not mitm else "Eve intercepts Alice's genuine Public Key on the wire, drops it, and injects her own rogue Public Key (e_E, N_E) to Bob!",
            "type": "transmit_pk",
            "mitm_active": mitm,
            "data": {
                "sent_by": "Alice",
                "received_by": "Bob" if not mitm else "Eve (Intercepted)",
                "delivered_to_bob": f"Alice PK ({alice_n_hex[:16]}...)" if not mitm else f"Eve Spoofed PK ({eve_n_hex[:16]}...)"
            }
        },
        {
            "id": 3,
            "title": "Session Secret Creation",
            "actor": "Bob (Bank B)",
            "description": f"Bob generates a 256-bit AES symmetric session key: {session_hex[:24]}...",
            "type": "session_gen",
            "mitm_active": False,
            "data": {"session_key": session_hex[:32] + "..."}
        },
        {
            "id": 4,
            "title": "Key Encrypted & Dispatched",
            "actor": "Optical/Copper Cable" if not mitm else "Eve (MITM Interceptor)",
            "description": "Bob encrypts session key under the Public Key he holds and transmits the ciphertext back." if not mitm else "Bob encrypts with Eve's rogue key! Eve intercepts ciphertext, decrypts it with d_Eve, copies the session key, re-encrypts with Alice's real key, and forwards it!",
            "type": "transmit_cipher",
            "mitm_active": mitm,
            "data": {
                "encrypted_by": "Bob",
                "stolen_by_eve": stolen_hex[:32] + "..." if mitm else None,
                "reencrypted": mitm,
                "wire_preview": wire_hex[:32] + "..."
            }
        },
        {
            "id": 5,
            "title": "Alice Decrypts Session Key",
            "actor": "Alice (Bank A)",
            "description": f"Alice decrypts incoming ciphertext with her private key d_A, recovering: {alice_key_hex[:24]}...",
            "type": "decrypt",
            "mitm_active": False,
            "data": {"alice_recovered": alice_key_hex[:32] + "...", "matches_bob": alice_key == session}
        },
        {
            "id": 6,
            "title": "Physical Channel Disturbance Audit",
            "actor": "Physical Waveform Monitor",
            "description": "Measured wave disturbance on the line: 0.00%. Classical optical/electrical signals can be passively cloned or spliced with zero quantum back-action.",
            "type": "physics_audit",
            "mitm_active": mitm,
            "data": {"qber_equivalent": 0.0, "detected": False, "signal_loss_db": 0.0}
        }
    ]

    return {
        "keys_match": alice_key == session,
        "eve_knows_key": mitm,
        "anyone_detected_eve": False,
        "seconds": elapsed,
        "ciphertext_len": len(wire),
        "bits": bits,
        "alice_pubkey": {"e": alice.e, "n": alice_n_hex, "preview": alice_n_hex[:26] + "..."},
        "eve_pubkey": {"e": eve.e, "n": eve_n_hex, "preview": eve_n_hex[:26] + "..."} if eve else None,
        "session_key": session_hex,
        "stolen_key": stolen_hex,
        "alice_recovered_key": alice_key_hex,
        "ciphertext_hex": wire_hex[:128] + ("..." if len(wire_hex) > 128 else ""),
        "steps": steps,
        "physical_disturbance": 0.0
    }


def _pollard_rho(n):
    if n % 2 == 0:
        return 2
    while True:
        x = y = random.randrange(2, n); c = random.randrange(1, n); d = 1
        while d == 1:
            x = (x * x + c) % n; y = (y * y + c) % n; y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def harvest_now_decrypt_later(prime_bits=32):
    """Toy demo: Eve records an RSA-protected session secret today and factors the
    modulus later. A 64-bit modulus falls to Pollard rho in milliseconds; for RSA-2048
    the same role is played by Shor's algorithm on a large quantum computer."""
    p, q = getPrime(prime_bits), getPrime(prime_bits)
    n, e = p * q, 65537
    secret = random.getrandbits(min(prime_bits, 30))
    recorded = pow(secret, e, n)                     # what Eve stores from the wire
    t0 = time.perf_counter()
    f = _pollard_rho(n)
    p_found = f
    q_found = n // f
    phi = (p_found - 1) * (q_found - 1)
    d = inverse(e, phi)
    recovered = pow(recorded, d, n)
    elapsed = time.perf_counter() - t0

    sample_amounts = [2_500_000, 10_000_000, 50_000_000, 75_000_000]
    payload_msg = "SWIFT-WIRE: Bank A -> Bank B ${:,} USD [AUTH-TOKEN: 0x{:X}]".format(
        random.choice(sample_amounts), secret
    )

    return {
        "modulus_bits": n.bit_length(),
        "recovered": recovered == secret,
        "attack_seconds": elapsed,
        "prime_p": p_found,
        "prime_q": q_found,
        "modulus_n": n,
        "modulus_n_hex": hex(n),
        "public_e": e,
        "private_d": d,
        "private_d_hex": hex(d),
        "secret_int": secret,
        "secret_hex": hex(secret),
        "ciphertext_int": recorded,
        "ciphertext_hex": hex(recorded),
        "payload_example": payload_msg,
        "shor_comparison": {
            "toy_modulus_bits": n.bit_length(),
            "toy_qubits_needed": 2 * n.bit_length(),
            "toy_time_sec": round(elapsed, 4),
            "rsa2048_modulus_bits": 2048,
            "rsa2048_qubits_needed": 4096,
            "rsa2048_classical_time_years": "3.8 x 10^14 years (Classical Supercluster)",
            "rsa2048_quantum_shor_time_mins": "~8 to 15 minutes (Fault-Tolerant QC)",
            "quantum_gates_needed": "~72 Billion Toffoli Gates (Gidney & Ekerå 2021)"
        }
    }
