# QBheem: College Project Viva & Oral Defense Preparation Guide
## High-Scoring Guide for University / College Viva, External Examiners & Project Defense

---

# TABLE OF CONTENTS
1. [The Elevator Pitch (Memorize This!)](#1-the-elevator-pitch)
   - 1.1 The 30-Second Version (Quick Intro)
   - 1.2 The 2-Minute Comprehensive Intro
2. [Golden Numbers & Formulas to Remember](#2-golden-numbers--formulas-to-remember)
3. [Top 25 Viva Questions & Perfect Model Answers](#3-top-25-viva-questions--perfect-model-answers)
   - [Category A: Project Concept & Problem Statement](#category-a-project-concept--problem-statement) (Q1 - Q5)
   - [Category B: Quantum Mechanics & BB84 Physics](#category-b-quantum-mechanics--bb84-physics) (Q6 - Q10)
   - [Category C: Classical Post-Processing & Algorithms](#category-c-classical-post-processing--algorithms) (Q11 - Q16)
   - [Category D: Implementation, Qiskit & System Architecture](#category-d-implementation-qiskit--system-architecture) (Q17 - Q21)
   - [Category E: Critical "Trap" Questions Examiners Love to Ask](#category-e-critical-trap-questions-examiners-love-to-ask) (Q22 - Q25)
4. [Live Project Demonstration Script (Step-by-Step)](#4-live-project-demonstration-script)
5. [Viva Defense Strategies (How to Handle Tough Questions)](#5-viva-defense-strategies)

---

## 1. The Elevator Pitch

When the external examiner sits down and says:  
> *"Tell me about your project in simple terms."*

Do **NOT** start by reading code or listing libraries. Use one of these structured pitches:

### 1.1 The 30-Second Version
> *"Good morning, Sir/Madam. Our project is titled **QBheem**, a Quantum-Secured Interbank Key Distribution and Transaction Defense platform.  
> Currently, global banks rely on RSA encryption, which will be completely broken once scalable quantum computers arrive using Shor's algorithm.  
> **QBheem** implements the **BB84 Quantum Key Distribution protocol** where Bank A and Bank B exchange keys using polarized photons. Due to the quantum **No-Cloning Theorem** and **wavefunction collapse**, any eavesdropping attempt by an adversary (Eve) alters the quantum states and creates an unmistakable error spike ($\sim 25\%$). If detected, QBheem immediately aborts the session before any money is transferred. We implemented this with a dual-engine architecture using both NumPy and IBM's Qiskit SDK, coupled with an interactive fintech dashboard."*

---

### 1.2 The 2-Minute Comprehensive Intro
> *"Today, trillions of dollars in interbank transfers are secured by classical asymmetric cryptography like RSA-2048. However, an adversary can record this encrypted data today and decrypt it in the future using Shor's algorithm on a quantum computer—this is called the **'Harvest Now, Decrypt Later'** threat.  
>
> Our project, **QBheem**, replaces computational security with **physics-based, information-theoretic security** using the BB84 protocol.  
>
> The system operates in three core phases:  
> 1. **Quantum Transmission:** Bank A (Alice) sends thousands of single qubits in randomly chosen rectilinear ($+$) or diagonal ($\times$) bases over an optical channel. Bob measures them in random bases.  
> 2. **Classical Post-Processing:** Alice and Bob perform basis sifting, parameter estimation to measure the Quantum Bit Error Rate (QBER), Cascade error correction, and Toeplitz hash privacy amplification to distill an untampered 256-bit AES key.  
> 3. **Application Defense:** The distilled key encrypts a $\$2.5\text{M}$ financial wire transfer using AES-256-GCM.  
>
> If an adversary taps the line, the error rate exceeds our mathematical threshold of $11\%$, and the system automatically withholds the key and halts the transfer. We have simulated this on both complex state-vectors and real Qiskit Clifford circuits, validated with 12 unit tests and interactive telemetry charts."*

---

## 2. Golden Numbers & Formulas to Remember

Examiners love asking about numbers and parameters. Keep these at your fingertips:

| Parameter | Value | Why this value? |
|---|---|---|
| **Raw Qubits ($n$)** | `16,384` (or `8,192`) | Sufficient sample size to survive sifting, sampling, and finite-key bounds. |
| **Sifting Retention Rate** | $\approx 50\%$ | Matching bases occur $\frac{1}{2}$ of the time when chosen uniformly at random. |
| **Clean Channel QBER** | $0.5\% - 1.5\%$ | Typical background depolarizing noise in optical fiber. |
| **Eve Intercept QBER** | $\approx 25\%$ | When Eve measures in the wrong basis ($50\%$), Bob has a $50\%$ chance of error ($0.5 \times 0.5 = 0.25$). |
| **Security Abort Threshold** | **$11.0\%$** | The asymptotic Shannon limit (Devetak-Winter bound) where Eve's mutual information equals Bob's. |
| **QBER Sample Fraction** | $20\%$ (`0.2`) | Sacrificed to estimate QBER; discarded so Eve cannot use them. |
| **Final Key Length** | `256` bits | Standard length for bank-grade AES-256-GCM encryption. |
| **Verification Tag** | `64` bits | SHA-256 digest to confirm keys match before application use. |

---

## 3. Top 25 Viva Questions & Perfect Model Answers

### Category A: Project Concept & Problem Statement

#### Q1: What is the main problem your project solves?
**Answer:** It addresses the vulnerability of classical public-key cryptography (like RSA and ECC) to quantum attacks via Shor's algorithm and the "Harvest Now, Decrypt Later" threat. We solve this by using Quantum Key Distribution (BB84), which guarantees security based on quantum physics rather than computational assumptions.

#### Q2: What is Quantum Key Distribution (QKD)?
**Answer:** QKD is a secure communication method that enables two parties to produce a shared random secret key known only to them. That key can then be used to encrypt and decrypt classical messages (e.g., using AES-256-GCM or One-Time Pad).

#### Q3: Does QKD transfer the actual bank money or the secret message over the quantum link?
**Answer:** **No, absolutely not.** QKD only distributes the *symmetric encryption key*. The actual encrypted financial payload (the bank wire) is transmitted over conventional high-speed classical networks (TCP/IP) encrypted with AES-256-GCM.

#### Q4: Why is your project named "QBheem"?
**Answer:** It carries a clever double meaning:
1. **Bheem the Protector:** Named after the legendary heroic protector, representing the system standing guard between Bank A and Bank B to protect against the adversary Eve.
2. **"Q-Beam" (Physics Pun):** Phonetically sounds like *Quantum Beam*, which is literally the polarized beam of single photons sent through the optical fiber.

#### Q5: What is the difference between Information-Theoretic Security and Computational Security?
**Answer:** 
* **Computational Security (RSA/ECC):** An adversary with infinite computing power or a quantum computer can break the encryption because security relies on the mathematical difficulty of prime factorization.
* **Information-Theoretic Security (BB84):** Security is proven mathematically using physics. Even an adversary with infinite computational power cannot break the key because the information was never present on the channel to be copied.

---

### Category B: Quantum Mechanics & BB84 Physics

#### Q6: Which fundamental quantum physics principles make BB84 secure?
**Answer:** Two fundamental laws:
1. **The No-Cloning Theorem:** An unknown quantum state cannot be cloned or duplicated without disturbing it.
2. **Heisenberg Uncertainty / Measurement Collapse:** Measuring an unknown quantum state irreversibly collapses its wavefunction into one of the eigenstates of the measurement basis, introducing measurable physical disturbance.

#### Q7: What are the two measurement bases used in BB84?
**Answer:**
1. **Rectilinear Basis ($+$):** States $|0\rangle$ and $|1\rangle$.
2. **Diagonal Basis ($\times$):** States $|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ and $|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$.
These two bases are **mutually unbiased**: knowing a state with certainty in one basis yields a completely random ($50/50$) outcome in the other.

#### Q8: Derive why Eve's intercept-resend attack introduces exactly 25% error.
**Answer:**
* Alice sends a qubit in basis A.
* Eve intercepts and must guess Bob’s/Alice’s basis. She chooses the wrong basis with probability $P = 0.5$.
* When Eve measures in the wrong basis, she projects the qubit into an orthogonal superposition and forwards her wrong measurement.
* Bob measures in Alice’s basis (which matches Alice). Because the qubit was rotated by Eve, Bob has a $50\%$ chance of measuring the incorrect bit value ($|\langle \text{wrong} | \text{Eve} \rangle|^2 = 0.5$).
* **Total Probability of Error:**
  $$P(\text{Eve wrong basis}) \times P(\text{Bob wrong outcome}) = 0.5 \times 0.5 = 0.25 = \mathbf{25\%}$$

#### Q9: What happens if Eve only intercepts 40% of the qubits?
**Answer:** Eve’s error scales linearly with her interception fraction:
$$\text{Expected QBER} \approx \text{Channel Noise} + (0.25 \times f)$$
For $f = 0.40$ ($40\%$), the induced error is $0.25 \times 0.40 = 10\%$. Combined with natural channel noise ($1\%$), the QBER reaches $\sim 11\%$, right at our cutoff boundary where finite-key bounds reject the session.

#### Q10: What is depolarizing noise in the quantum channel?
**Answer:** Depolarizing noise models the environmental decoherence and thermal polarization drift in optical fiber. With probability $p$, a photon is perturbed by one of the three Pauli operators ($X$ bit-flip, $Z$ phase-flip, or $Y$ both), producing a baseline error rate $\approx \frac{2}{3}p$.

---

### Category C: Classical Post-Processing & Algorithms

#### Q11: What is Basis Sifting?
**Answer:** After quantum transmission, Alice and Bob publicly announce their basis choices ($+$ or $\times$) over the classical channel. They **never** announce the bit values. Wherever their bases matched, they keep the bits (forming the *sifted key*). They discard all mismatched rounds.

#### Q12: Why do you sample 20% of the sifted key during Parameter Estimation?
**Answer:** To calculate the **Quantum Bit Error Rate (QBER)**. By randomly selecting $20\%$ of bits and publicly comparing them, we get a statistically accurate estimate of channel disturbance. These sampled bits are permanently discarded so an eavesdropper cannot use them.

#### Q13: Why is the threshold set to 11%? Where does this number come from?
**Answer:** In Shannon information theory, the secret key generation rate for BB84 with one-way post-processing is governed by the Devetak-Winter bound:
$$R = 1 - 2 h_2(\text{QBER})$$
where $h_2(p) = -p \log_2(p) - (1-p)\log_2(1-p)$ is the binary entropy function.  
Setting $R = 0$ gives $h_2(\text{QBER}) = 0.5$, which solves to **$\text{QBER} \approx 11.0\%$**. Above $11\%$, Eve has more mutual information about the key than Bob, and privacy amplification cannot produce a secure key.

#### Q14: How does the Cascade Error Correction algorithm work in your code?
**Answer:** Cascade is an interactive parity-check protocol:
1. Keys are divided into blocks of size $k \approx \frac{0.73}{\text{QBER}}$.
2. Alice and Bob calculate and compare the parity of each block.
3. If parities differ, an odd number of errors exists in that block. A recursive binary search (bisection) isolates and corrects the erroneous bit.
4. Additional shuffled permutation passes clean up remaining paired errors.
5. Every disclosed parity bit is counted as leaked information ($\text{leak}_{EC}$).

#### Q15: What is Privacy Amplification, and how does Toeplitz hashing work?
**Answer:** Privacy amplification compresses the error-corrected key to eliminate any partial information leaked during error correction or intercepted by Eve.  
In our project, it is implemented using a **Toeplitz matrix** over Galois Field $\text{GF}(2)$:
$$K_{secure} = (T \cdot K_{corrected}) \pmod 2$$
The Toeplitz matrix is a universal hash function parameterized by a public random seed generated *after* the quantum phase, reducing Eve’s information to less than $2^{-s}$.

#### Q16: What is the finite-key length bound formula in your code?
**Answer:** In [`postprocessing.py`](file:///c:/Users/jahir/Downloads/bb84_bank/bb84_bank/qkd/postprocessing.py), the distillable secure length $\ell$ is calculated as:
$$\ell = n \cdot [1 - h_2(q_{upper})] - \text{leaked}_{EC} - 2\log_2\left(\frac{1}{\epsilon_{sec}}\right)$$
where $q_{upper}$ incorporates a **Hoeffding bound margin** $\sqrt{\frac{\ln(1/\epsilon_{pe})}{2 n_{sample}}}$ to protect against statistical sample underestimation.

---

### Category D: Implementation, Qiskit & System Architecture

#### Q17: Why did you implement dual backends (NumPy and Qiskit)?
**Answer:**
* **NumPy (`qkd/quantum.py`):** Optimized vector operations simulating state vectors in Hilbert space $\mathbb{C}^2$. Runs in under $50\text{ ms}$ for 16,384 qubits, enabling instantaneous UI interactions and large Monte Carlo sweeps.
* **Qiskit (`qkd/quantum_qiskit.py`):** Builds real quantum circuits using IBM's Qiskit SDK with single-qubit gates and measurements, proving that our software is ready for execution on real quantum hardware or Qiskit Aer Stabilizer simulators.

#### Q18: Which simulator did you use in Qiskit and why?
**Answer:** We used `AerSimulator(method="stabilizer")`. Because BB84 uses only Clifford group operations (Hadamard gate $H$, Pauli-X gate $X$, Pauli-Z gate $Z$, and computational basis measurements), the **Gottesman-Knill theorem** allows us to simulate these circuits in polynomial time without the exponential memory overhead of full statevectors.

#### Q19: How is the application payload secured?
**Answer:** In [`qkd/application.py`](file:///c:/Users/jahir/Downloads/bb84_bank/bb84_bank/qkd/application.py), the distilled 256-bit key encrypts a structured JSON bank wire transfer using **AES-256-GCM** (Galois/Counter Mode). GCM provides **Authenticated Encryption with Associated Data (AEAD)**, ensuring both confidentiality and cryptographic integrity verification with a 128-bit authentication tag.

#### Q20: Explain the architecture of the web dashboard.
**Answer:**
* **Backend:** Python FastAPI running on Uvicorn, exposing RESTful endpoints (`/api/session`, `/api/health`, `/api/experiments/*`, `/api/rsa?mitm=...`, `/api/rsa/harvest`).
* **Frontend:** Responsive vanilla HTML5/CSS/JavaScript with glassmorphic dark-mode design, organized into 3 primary tabs:
  1. **Live Exchange:** Animated optical fiber SVG with moving photon wave packets, dual real-time terminals, QBER meter with 11% cutoff tick, and AES-256-GCM payload inspector.
  2. **Telemetry & Analysis:** Chart.js Monte Carlo empirical sweeps (QBER distributions, key distillation efficiency, partial intercept sweeps).
  3. **QBheem vs Classical RSA Visual Suite:** Fully interactive comparison featuring an animated Classical MitM packet pipeline, Eve rogue router tap, 6-stage stepper, 3 micro-terminals, Harvest-Now-Decrypt-Later Shor's algorithm lab with mathematical factoring cards, and a live Head-to-Head Duel Arena.

#### Q21: How many automated tests exist in your test suite?
**Answer:** We have **12 comprehensive unit tests** in [`tests/test_qkd.py`](file:///c:/Users/jahir/Downloads/bb84_bank/bb84_bank/tests/test_qkd.py) covering clean channel zero-error, 25% intercept-resend, linear partial intercepts, Cascade noise correction, Toeplitz hashing determinism, end-to-end AES wire transfer, ciphertext tampering detection, and RSA MITM vulnerabilities. All 12 tests pass 100%.

#### Q22: How does QBheem compare visually and theoretically with Classical RSA under attack?
**Answer:**
* **Classical RSA:** Tapping the line causes **0.00% physical signal perturbation**. Eve can execute a Man-in-the-Middle attack by substituting her public key $(e_E, N_E)$ and intercepting Bob's session key. Alice and Bob's keys match, so both banks proceed in total ignorance that Eve holds the private key (**Silent Failure**). Furthermore, classical ciphertexts stored today can be factored later by Shor's algorithm (**Harvest-Now-Decrypt-Later**).
* **QBheem (BB84 QKD):** Photons cannot be copied without measurement (**No-Cloning Theorem**). Eve's measurements inevitably collapse the superposition, causing a **~25% QBER spike**. Both banks immediately detect the intrusion, abort key release, and withhold the financial wire (**Physics-Enforced Fail-Safe Protection**). No unmeasured photons can be stored in Eve's vault, making QBheem 100% immune to HNDL.

---

### Category E: Critical "Trap" Questions Examiners Love to Ask

#### Q23: [TRAP] Can QKD transmit messages faster than light (Superluminal communication)?
**Answer:** **No, absolutely not.** QKD strictly respects Einstein's special theory of relativity. Sifting, parameter estimation, and error correction require classical communication over standard radio or fiber channels, which are bounded by the speed of light $c$.

#### Q24: [TRAP] Can Eve simply sit and passively listen to the optical fiber without touching the photons?
**Answer:** **No.** A classical wire allows an inductive magnetic clamp to read electrical signals without stopping current. But light consists of discrete quantum packets called **photons**. To detect a photon, Eve must physically absorb or measure it, which destroys or collapses its quantum state. There is no such thing as "passive non-destructive listening" on an unknown quantum state.

#### Q25: [TRAP] What is the major vulnerability of BB84 if used alone in the real world?
**Answer:** The **Classical Channel Authentication problem**. BB84 assumes Alice and Bob communicate their bases over an authenticated channel. If the classical channel is unauthenticated, Eve could execute a classical Man-in-the-Middle attack. In real-world deployment, this is prevented by using a small pre-shared symmetric key to authenticate classical messages with **Wegman-Carter MACs**.

#### Q26: [TRAP] Why can't we use standard classical amplifiers/repeaters to send QKD across thousands of kilometers?
**Answer:** Standard optical repeaters (like Erbium-Doped Fiber Amplifiers / EDFAs) work by stimulated emission, which makes clones of light pulses. By the **No-Cloning Theorem**, quantum states cannot be cloned. Amplifying a quantum signal destroys its entanglement and superposition. Therefore, long-distance QKD requires either **Trusted Relays (nodes)**, **Free-Space Satellite links**, or future **Quantum Repeaters** with quantum memory.

---

## 4. Live Project Demonstration Script

Follow this exact sequence during your live demo to get maximum marks:

### Step 1: Open the Dashboard
* Navigate to `http://127.0.0.1:8000`.
* Point to the top status pill:  
  *"Sir, as you can see here, our FastAPI backend is connected and healthy, confirming that the Qiskit quantum simulator is initialized."*

### Step 2: Run an Honest Exchange (Clean Channel)
1. Keep **Eve taps the line** UNCHECKED.
2. Click **Execute Exchange**.
3. Point to the UI:
   * **Terminal A & B:** Point out the basis matching log, error estimation, and the AES key generation.
   * **QBER Meter:** Show that the error rate is $\sim 0.8\%$, well below the amber $11\%$ threshold line.
   * **Sifting Funnel:** Explain how 16,384 raw qubits were sifted to $\sim 8,200$, sampled to $\sim 6,500$, and distilled to a secure key.
   * **Payload Card:** Show that Bank A's $\$2,500,000.00$ transfer was encrypted with AES-256-GCM, sent across, and Bank B verified the integrity tag.

### Step 3: Run the Adversary Attack (Eve Active)
1. Check the box **"Eve taps line (Intercept-Resend)"**.
2. Notice the center SVG fiber optic line immediately turns glowing red with a tapping laser indicator.
3. Click **Execute Exchange**.
4. Point to the outcome:
   * **Verdict:** Highlights **"⛔ Security Abort — Zero Keys Released"**.
   * **QBER Meter:** Spikes to $\sim 25\%$, easily crossing the $11\%$ threshold.
   * **Protected Payload:** Displays **"Transfer withheld. QBheem detected channel compromise — no wire was transmitted."**
   * *Say to the examiner:* *"Because the error rate hit 25%, quantum mechanics proved to both banks that an eavesdropper was present. No transaction key was ever released, meaning the bank's money is 100% safe."*

### Step 4: Show the Comparison Tab ("QBheem vs Classical RSA")
1. Click the **QBheem vs Classical RSA** tab.
2. Demonstrate the **Classical RSA & MitM Pipeline**:
   * Click **Launch MitM Attack (Eve)**:
     - Watch the **animated packet traverse the wire conduit** and get intercepted by Eve's rogue router.
     - Show the **Step-by-Step progress tracker** (KeyGen → PK Wire → Session Secret → Ciphertext → Decrypt → Audit).
     - Point out the **3 Micro-Terminals**: Bank A terminal, Wire & Eve Sniffer terminal (showing stolen AES key: `0x...`), and Bank B terminal.
     - Show the physical layer verdict: **Physical Waveform Disturbance = 0.00%**, **Was Eve detected? NO**.
     - *Explain:* *"Classical RSA has zero physical feedback when someone taps or swaps keys. Both banks proceed blindly believing their session was secure, while Eve decrypts every transaction."*
3. Demonstrate the **Harvest-Now-Decrypt-Later (HNDL) & Shor's Factorization Lab**:
   * Switch to sub-tab **2. Harvest-Now-Decrypt-Later & Shor**.
   * Show the 3-Era timeline (Present 2026 Capture → Vault Storage → Q-Day Factorization).
   * Click **Execute Quantum Modulus Factorization**:
     - Point out the live mathematical cards displaying target modulus $N$, prime factors $p$ and $q$ extracted via $\gcd(a^{r/2} \pm 1, N)$, Euler's totient $\phi(N)$, private exponent $d$, and the unlocked SWIFT banking payload.
     - Highlight the **QBheem Immunity Shield**: Why BB84 is 100% immune (No-Cloning Theorem prevents saving unmeasured photons; measurement causes immediate 25% QBER abort; zero keys exist in Eve's vault).
4. Demonstrate the **Live Head-to-Head Arena (RSA vs QBheem)**:
   * Switch to sub-tab **3. Live Head-to-Head Arena**.
   * Click **Simulate Simultaneous Attack on Both Networks**:
     - Left column (Classical RSA): 0% disturbance, Eve holds session key, funds silently compromised.
     - Right column (QBheem BB84 QKD): QBER spikes to ~25% crossing the 11% threshold, instant security alarm, zero keys released, funds 100% safe.

---

## 5. Viva Defense Strategies

1. **If you don't know the exact answer to a question:**
   * **Do NOT guess or make up physics:**  
     *Good response:* *"Sir, while I haven't implemented that specific variation, I know that in our BB84 implementation, we model this through [relate back to QBER or No-Cloning theorem]. I would be glad to explore that in our future roadmap."*
2. **If an examiner challenges you on why you didn't run on a real IBM quantum computer:**
   * *Answer:* *"Sir, IBM Quantum cloud devices have long queue times (often 30 to 60 minutes per job), which is impractical for real-time interbank transaction simulations. Furthermore, BB84 circuits consist entirely of Clifford gates, so under the Gottesman-Knill theorem, the Qiskit Aer Stabilizer simulator gives mathematically exact results with zero queuing delay."*
3. **If asked about team contribution:**
   * Clearly explain how the project is modularized: Quantum layer (`quantum.py`), Post-processing (`postprocessing.py`), Cryptographic application (`application.py`), and the FastAPI/Dashboard full-stack integration.
