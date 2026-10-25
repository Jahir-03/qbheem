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
    if mitm:
        stolen = PKCS1_OAEP.new(eve).decrypt(wire)
        wire = PKCS1_OAEP.new(pub).encrypt(stolen)         # re-encrypt for Alice
    alice_key = PKCS1_OAEP.new(alice).decrypt(wire)
    return {"keys_match": alice_key == session, "eve_knows_key": mitm,
            "anyone_detected_eve": False, "seconds": time.perf_counter() - t0,
            "ciphertext_len": len(wire)}


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
    secret = random.getrandbits(prime_bits)
    recorded = pow(secret, e, n)                     # what Eve stores from the wire
    t0 = time.perf_counter()
    f = _pollard_rho(n)
    d = inverse(e, (f - 1) * (n // f - 1))
    recovered = pow(recorded, d, n)
    return {"modulus_bits": n.bit_length(), "recovered": recovered == secret,
            "attack_seconds": time.perf_counter() - t0}
