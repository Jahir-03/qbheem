"""Module 1 (Qiskit backend) - the same BB84 quantum layer, run on real Qiskit circuits.

Every BB84 state and operation here (X, H, Pauli noise, Z-basis measurement) is Clifford, so
Aer's stabilizer simulator is exact. Qubits never interact, so the n rounds are split into
small independent circuits (CHUNK qubits each) and run as one batch - that keeps the cost
linear in n instead of blowing up with one giant tableau.

Eve is modelled in two executions:
  1. Alice's states -> Eve's basis rotation -> measurement          (Eve's bits)
  2. Eve re-prepares what she saw -> channel noise -> Bob's basis rotation -> measurement
Qubits Eve doesn't touch are re-prepared from Alice's (bit, basis) in stage 2, which gives
exactly the state they would have had passing through untouched.
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from .quantum import QuantumRun, random_bits

_SIM = AerSimulator(method="stabilizer")
CHUNK = 128
_NOISE_GATES = ("x", "y", "z")


def _execute(bits, bases, paulis, rot_bases):
    """Prepare |bit> in `bases`, apply Pauli (-1 = none), rotate into `rot_bases`, measure Z."""
    n = len(bits)
    circuits = []
    for s in range(0, n, CHUNK):
        e = min(s + CHUNK, n)
        qc = QuantumCircuit(e - s, e - s)
        for j in range(e - s):
            i = s + j
            if bits[i]:
                qc.x(j)
            if bases[i]:
                qc.h(j)
            if paulis[i] >= 0:
                getattr(qc, _NOISE_GATES[paulis[i]])(j)
            if rot_bases[i]:
                qc.h(j)
        qc.measure(range(e - s), range(e - s))
        circuits.append(qc)
    result = _SIM.run(circuits, shots=1, memory=True).result()
    out = np.zeros(n, dtype=np.uint8)
    for k, s in enumerate(range(0, n, CHUNK)):
        mem = result.get_memory(k)[0].replace(" ", "")      # Qiskit prints clbit m-1 ... clbit 0
        out[s:s + len(mem)] = [int(c) for c in reversed(mem)]
    return out


def transmit_qiskit(n, rng, eve_active=False, eve_fraction=1.0, noise=0.0):
    a_bits, a_bases = random_bits(n, rng), random_bits(n, rng)
    none = np.full(n, -1, dtype=int)
    eve_mask = np.zeros(n, dtype=bool)
    e_bits = np.zeros(n, dtype=np.uint8)
    e_bases = np.zeros(n, dtype=np.uint8)

    if eve_active:
        eve_mask = rng.random(n) < eve_fraction
        e_bases = random_bits(n, rng)
        e_bits = _execute(a_bits, a_bases, none, e_bases)        # Eve measures in her random basis

    send_bits = np.where(eve_mask, e_bits, a_bits).astype(np.uint8)
    send_bases = np.where(eve_mask, e_bases, a_bases).astype(np.uint8)
    paulis = none
    if noise > 0:
        hit = rng.random(n) < noise
        paulis = np.where(hit, rng.integers(0, 3, n), -1)
    b_bases = random_bits(n, rng)
    b_bits = _execute(send_bits, send_bases, paulis, b_bases)
    return QuantumRun(a_bits, a_bases, b_bases, b_bits, eve_mask, e_bits, e_bases)
