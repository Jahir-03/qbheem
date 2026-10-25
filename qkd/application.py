"""Module 3 - Use the QKD key to protect an interbank transaction (AES-256-GCM)."""
import json
from datetime import datetime, timezone
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

AAD = b"interbank-transfer-v1"


def make_transaction(amount=2_500_000.00):
    return {"sender_bank": "Bank A", "receiver_bank": "Bank B",
            "amount": amount, "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat()}


def encrypt_transaction(key: bytes, tx: dict) -> dict:
    c = AES.new(key, AES.MODE_GCM, nonce=get_random_bytes(12))
    c.update(AAD)
    ct, tag = c.encrypt_and_digest(json.dumps(tx).encode())
    return {"nonce": c.nonce.hex(), "ciphertext": ct.hex(), "tag": tag.hex()}


def decrypt_transaction(key: bytes, packet: dict) -> dict:
    c = AES.new(key, AES.MODE_GCM, nonce=bytes.fromhex(packet["nonce"]))
    c.update(AAD)
    return json.loads(c.decrypt_and_verify(bytes.fromhex(packet["ciphertext"]),
                                           bytes.fromhex(packet["tag"])))
