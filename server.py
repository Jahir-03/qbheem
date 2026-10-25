"""FastAPI backend: the dashboard talks to the real Python/Qiskit code through this API.

Run:  uvicorn server:app --reload      then open http://127.0.0.1:8000
"""
import hashlib, os, time
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from qkd.protocol import SessionConfig, run_session, KEY_BITS
from qkd.application import make_transaction, encrypt_transaction, decrypt_transaction
from qkd import experiments, rsa_baseline

try:
    import qiskit, qiskit_aer  # noqa: F401
    QISKIT = True
except ImportError:
    QISKIT = False

HERE = os.path.dirname(__file__)
app = FastAPI(title="QBheem - Quantum Interbank Protection")


class SessionReq(BaseModel):
    n_qubits: int = Field(16384, ge=512, le=65536)
    eve_active: bool = False
    eve_fraction: float = Field(1.0, ge=0, le=1)
    noise: float = Field(0.01, ge=0, le=0.3)
    backend: str = Field("numpy", pattern="^(numpy|qiskit)$")
    seed: int | None = None
    amount: float = 2_500_000.0


class QberReq(BaseModel):
    trials: int = Field(20, ge=2, le=100)
    noise: float = Field(0.02, ge=0, le=0.1)
    n_qubits: int = Field(16384, ge=2048, le=32768)


@app.get("/api/health")
def health():
    return {"ok": True, "qiskit": QISKIT, "key_bits": KEY_BITS}


@app.post("/api/session")
def session(req: SessionReq):
    if req.backend == "qiskit":
        if not QISKIT:
            raise HTTPException(400, "Qiskit is not installed on the server (pip install qiskit qiskit-aer)")
    t0 = time.perf_counter()
    r = run_session(SessionConfig(n_qubits=req.n_qubits, eve_active=req.eve_active, eve_fraction=req.eve_fraction,
                                  noise=req.noise, backend=req.backend, seed=req.seed))
    out = {
        "seconds": round(time.perf_counter() - t0, 2), "backend": req.backend,
        "stats": {"raw": r.n_raw, "sifted": r.n_sifted, "sampled": r.n_sample, "after_sampling": r.n_after_pe,
                  "leaked_ec": r.leaked_ec, "secure_len": r.secure_len, "qber": r.qber},
        "threshold": r.config.qber_threshold, "aborted": r.aborted, "reason": r.reason, "log": r.log,
        "eve_accuracy": r.eve_sifted_accuracy, "transaction": None,
    }
    if r.success:                                    # Module 3: use the key
        tx = make_transaction(req.amount)
        packet = encrypt_transaction(r.alice_key, tx)
        try:
            received, ok = decrypt_transaction(r.bob_key, packet), True
        except ValueError:
            received, ok = None, False
        out["transaction"] = {"sent": tx, "packet": packet, "received": received, "verified": ok,
                              "key_fingerprint": hashlib.sha256(r.alice_key).hexdigest()[:16]}
    return out


@app.post("/api/experiments/qber")
def exp_qber(req: QberReq):
    return experiments.qber_runs(req.trials, req.n_qubits, req.noise)


@app.get("/api/experiments/efficiency")
def exp_eff():
    return experiments.efficiency_vs_noise()


@app.get("/api/experiments/intercept")
def exp_intercept():
    return experiments.intercept_sweep()


@app.get("/api/rsa")
def rsa(mitm: bool = False):
    return rsa_baseline.rsa_handshake(mitm=mitm)


@app.get("/api/rsa/harvest")
def rsa_harvest():
    return rsa_baseline.harvest_now_decrypt_later()


app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")


@app.get("/")
def index():
    return FileResponse(os.path.join(HERE, "static", "index.html"))
