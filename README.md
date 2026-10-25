# BB84 interbank key exchange

Bank A (Alice) and Bank B (Bob) agree on a 256-bit AES key over a simulated quantum link, then use it to encrypt a transfer. Eve can tap the line. The dashboard is a plain HTML page that calls a FastAPI backend, which runs the real Python code (NumPy or Qiskit).

## Run it

```bash
pip install -r requirements.txt
uvicorn server:app --reload          # then open http://127.0.0.1:8000
```

Other entry points:

```bash
python demo.py [--qiskit]            # CLI walkthrough: honest run, Eve run, RSA baseline
python -m qkd.experiments            # regenerates the PNGs in figures/
python -m pytest -q                  # 12 tests, NumPy and Qiskit backends
```

## Layout

| Path | What it does |
|---|---|
| `qkd/quantum.py` | Module 1. Random bits/bases, encoding, intercept-resend Eve (full or partial), depolarizing noise, Bob's measurement. NumPy state vectors. |
| `qkd/quantum_qiskit.py` | Module 1 on real Qiskit circuits (Aer stabilizer simulator, exact for BB84's Clifford gates). Same interface, so it is a drop-in backend. |
| `qkd/postprocessing.py` | Module 2. Sifting, QBER sampling, simplified Cascade, verification tag, finite-key length bound, Toeplitz privacy amplification. |
| `qkd/protocol.py` | Runs one full session and aborts if QBER > 11% or the secure length is under 256 bits. |
| `qkd/application.py` | Module 3. AES-256-GCM encrypt/decrypt of a JSON transaction (PyCryptodome). |
| `qkd/experiments.py`, `qkd/rsa_baseline.py` | Module 4. Experiments for the charts, plus the RSA handshake, MITM and toy record-now-break-later attack. |
| `server.py` | FastAPI app. `POST /api/session`, `POST /api/experiments/qber`, `GET /api/experiments/efficiency`, `GET /api/experiments/intercept`, `GET /api/rsa`, `GET /api/rsa/harvest`, `GET /api/health`. |
| `static/index.html` | The dashboard. Chart.js is vendored in `static/vendor/`, so it works offline. |
| `REPORT.md` | Security analysis and BB84+AES vs RSA comparison, with numbers from this code. |

## What is and is not modelled

Modelled: intercept-resend attacks (any fraction of qubits), depolarizing channel noise, sifting, sampling-based QBER, error correction leakage, finite-size penalty, Toeplitz privacy amplification, authenticated encryption of the payload.

Not modelled, and worth saying in your write-up:

- The classical channel is assumed authenticated. Real BB84 authenticates it with a Wegman-Carter MAC using a small pre-shared key. Without that, Eve can sit in the middle of the classical channel.
- Single-photon ideal sources and detectors. Real systems have multi-photon pulses (photon-number-splitting attacks, handled with decoy states), detector blinding and other side channels.
- The secure-length formula is a simplified finite-key estimate, not a full composable security proof. Treat it as a sound teaching model, not as something to deploy.
- Cascade here has no back-tracking, so it leaks somewhat more than textbook Cascade.
- Qubit loss and distance attenuation.

## Ideas to extend it

Decoy-state BB84, photon loss by distance, a Wegman-Carter authenticated classical channel, a second attack (photon-number splitting or beam-splitting), key refresh and rate over time for a stream of transactions.
