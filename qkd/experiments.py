"""Module 4 - analysis. Pure-data functions (used by the API) plus a CLI that saves PNGs."""
import os, time
import numpy as np
from .protocol import SessionConfig, run_session
from .postprocessing import QBER_THRESHOLD


def qber_runs(trials=30, n_qubits=16384, noise=0.02, eve_fraction=1.0, seed=0):
    """QBER across repeated sessions, with and without Eve."""
    out = {"threshold": QBER_THRESHOLD, "no_eve": [], "eve": [], "aborted_no_eve": 0, "aborted_eve": 0}
    for t in range(trials):
        for key, eve in (("no_eve", False), ("eve", True)):
            r = run_session(SessionConfig(n_qubits=n_qubits, eve_active=eve, eve_fraction=eve_fraction,
                                          noise=noise, seed=seed * 100000 + t * 2 + eve))
            out[key].append(r.qber)
            out["aborted_" + key] += int(r.aborted)
    return out


def efficiency_vs_noise(noises=(0, .01, .02, .03, .05, .08, .12, .16), n_qubits=16384, trials=5, seed=1):
    """Raw bits -> sifted -> after sampling -> secure key length, per noise level."""
    rows = []
    for p in noises:
        rs = [run_session(SessionConfig(n_qubits=n_qubits, noise=p, seed=seed * 1000 + i)) for i in range(trials)]
        rows.append({"noise": p, "qber": float(np.mean([r.qber for r in rs])),
                     "raw": n_qubits, "sifted": float(np.mean([r.n_sifted for r in rs])),
                     "after_sampling": float(np.mean([r.n_after_pe for r in rs])),
                     "secure": float(np.mean([r.secure_len for r in rs])),
                     "abort_rate": float(np.mean([r.aborted for r in rs]))})
    return rows


def intercept_sweep(fractions=(0, .1, .2, .3, .4, .5, .75, 1.0), n_qubits=16384, noise=0.01, trials=10, seed=2):
    """How much of the line Eve taps vs. QBER, detection, and what she learns."""
    rows = []
    for f in fractions:
        rs = [run_session(SessionConfig(n_qubits=n_qubits, eve_active=f > 0, eve_fraction=f, noise=noise,
                                        seed=seed * 1000 + i)) for i in range(trials)]
        rows.append({"fraction": f, "qber": float(np.mean([r.qber for r in rs])),
                     "abort_rate": float(np.mean([r.aborted for r in rs])),
                     "key_produced_rate": float(np.mean([r.alice_key is not None for r in rs])),
                     "eve_accuracy": float(np.mean([r.eve_sifted_accuracy for r in rs])) if f > 0 else None})
    return rows


def _save_pngs(outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(outdir, exist_ok=True)

    d = qber_runs(trials=30)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(np.array(d["no_eve"]) * 100, bins=15, alpha=.8, label="No Eve (2% channel noise)")
    ax.hist(np.array(d["eve"]) * 100, bins=15, alpha=.8, label="Eve intercept-resend")
    ax.axvline(QBER_THRESHOLD * 100, color="k", ls="--", label="11% abort threshold")
    ax.set_xlabel("QBER (%)"); ax.set_ylabel("sessions"); ax.legend(); ax.set_title("QBER with and without an eavesdropper")
    fig.tight_layout(); fig.savefig(f"{outdir}/qber_eve_vs_clean.png", dpi=150); plt.close(fig)

    rows = efficiency_vs_noise()
    fig, ax = plt.subplots(figsize=(7, 4))
    x = [r["noise"] * 100 for r in rows]
    for k, lab in (("raw", "raw qubits"), ("sifted", "sifted"), ("after_sampling", "after QBER sampling"), ("secure", "final secure key")):
        ax.plot(x, [r[k] for r in rows], marker="o", label=lab)
    ax.set_xlabel("channel depolarizing noise (%)"); ax.set_ylabel("bits"); ax.legend(); ax.set_title("Key generation efficiency")
    fig.tight_layout(); fig.savefig(f"{outdir}/key_efficiency.png", dpi=150); plt.close(fig)

    rows = intercept_sweep()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot([r["fraction"] * 100 for r in rows], [r["qber"] * 100 for r in rows], marker="o", label="QBER (%)")
    ax.plot([r["fraction"] * 100 for r in rows], [r["key_produced_rate"] * 100 for r in rows], marker="s", label="sessions that produced a key (%)")
    ax.axhline(QBER_THRESHOLD * 100, color="k", ls="--")
    ax.set_xlabel("fraction of qubits Eve intercepts (%)"); ax.legend(); ax.set_title("Partial eavesdropping")
    fig.tight_layout(); fig.savefig(f"{outdir}/intercept_sweep.png", dpi=150); plt.close(fig)
    return rows


if __name__ == "__main__":
    t = time.time()
    rows = _save_pngs(os.path.join(os.path.dirname(__file__), "..", "figures"))
    for r in rows:
        print(r)
    print(f"saved figures in {time.time() - t:.1f}s")
