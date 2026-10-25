# QBheem: BB84 + AES-256 vs Classical RSA Key Exchange

All numbers come from this repository (16,384 qubits per session, 20% of the sifted key sampled for QBER, 1-2% depolarizing noise unless stated). Re-run `python -m qkd.experiments` to regenerate the figures in `figures/`.

## 1. Setup

Bank A sends qubits to Bank B over a fiber link. Eve may sit on the line and run an intercept-resend attack: she measures each qubit in a random basis and forwards a fresh qubit in what she saw. The banks sift, sample part of the sifted key to estimate the quantum bit error rate (QBER), correct the remaining errors, then hash the key down with privacy amplification. The result is used as an AES-256-GCM key for the transfer.

## 2. Security analysis: why QBER exposes Eve

When Eve guesses the basis wrong (50% of the time) she randomizes the qubit, and Bob then gets the wrong bit half the time on matching-basis rounds. So full interception gives an expected QBER of 0.5 x 0.5 = 25%. Intercepting a fraction f of the qubits gives about 25% x f on top of channel noise.

| Condition | Measured QBER | Outcome |
|---|---|---|
| No Eve, 2% channel noise (30 sessions) | mean 1.3%, max 1.7% | 0 of 30 aborted |
| Eve on every qubit, 2% noise (30 sessions) | mean 25.6%, min 23.8% | 30 of 30 aborted |

Partial interception (1% noise, 10 sessions per row):

| Eve intercepts | QBER | Sessions that produced a key | Share of sifted bits Eve guessed right |
|---|---|---|---|
| 0% | 0.7% | 100% | n/a |
| 10% | 3.4% | 100% | 53% |
| 20% | 5.6% | 0% | 55% |
| 40% | 10.5% | 0% | 60% |
| 100% | 25.3% | 0% | 75% |

Two things to point out in the write-up. First, the 11% threshold is not the only gate: at 20-40% interception the QBER is still under 11%, but the finite-key length bound drops below 256 bits and the session ends without a key. Second, when a light tap does slip through (10%), privacy amplification is what removes Eve's partial knowledge, because the key length is computed from the observed error rate.

See `figures/qber_eve_vs_clean.png` and `figures/intercept_sweep.png`.

## 3. Key generation efficiency

| Channel noise | QBER | Sifted | After sampling | Final secure bits |
|---|---|---|---|---|
| 0% | 0.0% | 8,161 | 6,529 | 3,788 |
| 1% | 0.6% | 8,207 | 6,566 | 3,383 |
| 2% | 1.3% | 8,207 | 6,566 | 2,793 |
| 3% | 2.0% | 8,207 | 6,566 | 1,964 |
| 5% | 3.4% | 8,207 | 6,566 | 813 |
| 8% and up | 5.7%+ | 8,207 | 6,566 | 0 |

Sifting halves the raw bits and sampling removes another 20%. Past roughly 5% depolarizing noise the combined cost of error correction and the finite-size margin eats the whole key, well before the 11% asymptotic limit. That gap is normal for finite block sizes. A larger block (more qubits per session) narrows it. See `figures/key_efficiency.png`.

## 4. BB84 + AES vs RSA

| | RSA key exchange | BB84 + AES-256 |
|---|---|---|
| Security assumption | Factoring is hard | Measuring a quantum state disturbs it |
| Eavesdropper detection | None. A passive copy leaves no trace; in the demo a man in the middle swapped the public key and neither bank noticed | Built in. Tapping raises QBER and the session aborts before a key is used |
| Recorded traffic | Can be stored and decrypted once factoring is practical (toy 64-bit modulus factored in ~0.1 s; Shor's algorithm plays this role for RSA-2048) | The key never crosses the wire, so recorded traffic holds nothing to decrypt later |
| Why it matters for banks | Settlement records and customer data stay sensitive for decades | Protects data whose confidentiality must outlast today's cryptography |
| Requirements | Certificates and a PKI | Quantum link (fiber, about 100 km per hop without trusted nodes), authenticated classical channel, specialized hardware |
| Weak points | Future quantum computers; implementation bugs | Side channels in real devices, authentication bootstrap, cost, distance |

Fair framing for the report: RSA with certificates does stop impersonation, and post-quantum algorithms (ML-KEM and similar) also address the record-now-decrypt-later risk without special hardware. The differentiator that BB84 adds is detection of tapping by physics rather than by computational assumption, which is what this project demonstrates. It does not replace the need for authentication.

## 5. Limitations

See the list at the end of the README. The main caveats: ideal single-photon source, authenticated classical channel assumed, and a simplified finite-key bound rather than a full composable proof.
