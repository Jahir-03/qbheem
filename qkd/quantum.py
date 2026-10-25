"""Module 1 - Quantum layer.

Qubits are simulated as 2-component complex state vectors. Basis 0 is the
rectilinear (+) basis {|0>, |1>}; basis 1 is the diagonal (x) basis {|+>, |->}.
"""
from dataclasses import dataclass
import numpy as np

S2 = 1 / np.sqrt(2)
# _STATES[bit, basis] -> 2-vector
_STATES = np.array([[[1, 0], [S2, S2]],
                    [[0, 1], [S2, -S2]]], dtype=complex)

_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def random_bits(n, rng):
    return rng.integers(0, 2, n, dtype=np.uint8)


def encode(bits, bases):
    """Encode each bit as a polarization state in the chosen basis."""
    return _STATES[bits, bases]


def measure(states, bases, rng):
    """Projective measurement of each qubit in the given basis (Born rule)."""
    a0, a1 = states[:, 0], states[:, 1]
    amp_one = np.where(bases == 0, a1, (a0 - a1) * S2)  # |1> or |-> amplitude
    p_one = np.abs(amp_one) ** 2
    return (rng.random(len(bases)) < p_one).astype(np.uint8)


def depolarize(states, p, rng):
    """With probability p, hit a qubit with a random Pauli (X, Y or Z).
    Observed bit-error rate is roughly 2p/3."""
    if p <= 0:
        return states
    hit = rng.random(len(states)) < p
    which = rng.integers(0, 3, len(states))
    out = states.copy()
    for k, P in enumerate((_X, _Y, _Z)):
        m = hit & (which == k)
        if m.any():
            out[m] = states[m] @ P.T
    return out


@dataclass
class QuantumRun:
    alice_bits: np.ndarray
    alice_bases: np.ndarray
    bob_bases: np.ndarray
    bob_bits: np.ndarray
    eve_mask: np.ndarray    # which qubits Eve intercepted
    eve_bits: np.ndarray    # what Eve measured (valid where eve_mask)
    eve_bases: np.ndarray


def transmit(n, rng, eve_active=False, eve_fraction=1.0, noise=0.0):
    """Alice -> (optional Eve) -> Bob over a noisy fiber channel.

    eve_fraction < 1 models a partial intercept-resend attack.
    """
    a_bits = random_bits(n, rng)
    a_bases = random_bits(n, rng)
    states = encode(a_bits, a_bases)

    eve_mask = np.zeros(n, dtype=bool)
    e_bits = np.zeros(n, dtype=np.uint8)
    e_bases = np.zeros(n, dtype=np.uint8)
    if eve_active:
        eve_mask = rng.random(n) < eve_fraction
        e_bases = random_bits(n, rng)
        e_bits = measure(states, e_bases, rng)
        resent = encode(e_bits, e_bases)          # Eve re-sends what she saw
        states = np.where(eve_mask[:, None], resent, states)

    states = depolarize(states, noise, rng)
    b_bases = random_bits(n, rng)
    b_bits = measure(states, b_bases, rng)
    return QuantumRun(a_bits, a_bases, b_bases, b_bits, eve_mask, e_bits, e_bases)
