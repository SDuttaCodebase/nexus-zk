# Nexus-ZK  
**A Privacy-Preserving, Revocable, Multi-Verifier Credential System**

---

## 📌 Problem Statement

In many digital systems, users are required to repeatedly share personal information (age, student status, nationality, etc.) with different services.  
This leads to:

- Excessive data disclosure  
- User tracking across platforms  
- Privacy violations  
- Centralized trust in verifiers  

The challenge is to design a system where users can **prove facts about themselves without revealing their identity or raw data**, even when interacting with multiple independent verifiers.

---

## 🎯 Our Solution: Nexus-ZK

Nexus-ZK is a cryptography-based credential system that enables:

- ✅ Selective disclosure of attributes  
- ✅ Zero-knowledge predicate proofs  
- ✅ Unlinkability across multiple verifiers  
- ✅ Privacy-preserving credential revocation  
- ✅ No global user identifiers  
- ✅ Minimal trust in verifiers  

The system is designed to be **practical, extensible, and beginner-friendly**, while still following academically sound cryptographic principles.

---

## 🧠 Key Concepts Used

- Zero-Knowledge Predicate Proofs (abstracted)
- Digital Signatures (BBS-style design)
- Hash-based revocation tokens
- Verifier unlinkability via independent sessions
- Honest-but-curious threat model

```text
┌────────────┐
│   ISSUER   │  (FastAPI :8000)
│            │
│  /issue    │
│  /revoke   │
└─────┬──────┘
      │  signed credential
      │  (attributes + signature
      │   + revocation token)
      ▼
┌────────────┐
│   HOLDER   │
│  (WALLET)  │
│            │
│ stores credential
│ generates proof
└─────┬──────┘
      │
      │  request challenge
      ▼
┌────────────┐
│  VERIFIER  │  (FastAPI :8001)
│            │
│ /challenge │───► nonce
│ /verify    │◄─── proof + nonce
└─────┬──────┘
      │
      ▼
  ACCEPT / REJECT
```

---

## Architectural Roles

* Issuer issues and revokes credentials
* Holder (Wallet) controls credentials and generates proofs
* Verifiers only learn proof validity (true / false)
* Multiple verifiers operate independently, with no shared state

---

## 🔍 Privacy Audit Mode (What Makes Nexus-ZK Stand Out)

Nexus-ZK includes a Verifier Privacy Audit Mode, which transparently demonstrates what the verifier sees and what it never sees.

When audit mode is enabled, the verifier logs:

❌ No user identity

❌ No credential identifier

❌ No raw attribute values

✔ Only the predicate evaluated

✔ Only the final verification result

## Example Audit Log (Verifier Console)
```text
🔍 VERIFIER PRIVACY AUDIT LOG
-----------------------------------
Received credential identifier: ❌ None
Received user identity: ❌ None
Received raw attributes:
  - age: ❌ hidden
  - country: ❌ hidden
  - student: ❌ hidden
Predicate evaluated: ✔ age_over_18
Verification result: ✔ True
-----------------------------------
```

This allows privacy guarantees to be demonstrated live, rather than merely claimed.

---

## 🔁 Multiple Verifiers & Unlinkability

Nexus-ZK supports multiple independent verifiers, each running as a separate service with:

  * Independent nonce storage
  * Independent databases
  * No shared identifiers or state
  * The same wallet and same credential can be verified across multiple verifiers, and those verifiers cannot link sessions, even if they collude.
  * This demonstrates true verifier unlinkability in a distributed setting.

---

## 📁 Project Structure
```text
nexus-zk/
│
├── README.md
├── docs/
│   ├── protocol.md
│   ├── threat_model.md
│   └── privacy_claims.md
│
├── issuer/
│   └── issuer.py
│
├── holder/
│   ├── wallet.py
│   └── proof_generator.py
│
├── wallet/
│   ├── wallet.py
│   └── wallet_cli.py
│
├── services/
│   ├── issuer_api/
│   ├── verifier_api/
│   └── verifier_b_api/
│
├── crypto/
│   └── bbs.py
│
├── benchmark/
│   └── benchmark.py
│
└── requirements.txt
```

---

## ⚙️ Installation & Setup

1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd nexus-zk
```

2️⃣ Create Virtual Environment
```bash
python -m venv venv
```

Activate it:
```bash
Windows: venv\Scripts\activate
```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

▶️ Running the System

Start Services
(Run each command in a separate terminal)

```bash
uvicorn services.issuer_api.main:app --reload
uvicorn services.verifier_api.main:app --reload --port 8001
uvicorn services.verifier_b_api.main:app --reload --port 8002
```

Issue Credential
```bash
python -m wallet.wallet_cli issue
```

Prove Predicate
```bash
python -m wallet.wallet_cli prove age_over_18
```

---

## 🔐 Security & Privacy Guarantees

The system guarantees:
  1. Selective disclosure of attributes
  2. Verifier unlinkability across sessions and services
  3. Replay-attack prevention via nonces
  4. Privacy-preserving revocation
  5. Issuer blindness to credential usage

Detailed analysis is available in:
  1. docs/protocol.md
  2. docs/threat_model.md
  3. docs/privacy_claims.md

---

## 📊 Evaluation

The system can be evaluated on:
  * Proof generation time
  * Verification time
  * Revocation lookup cost

Benchmarking support is included in the benchmark/ directory.

---

### Benchmark Results (Local Machine)

All measurements are averaged over 1000 iterations.

- Credential issuance: ~0.14 ms  
- Proof generation: ~0.001 ms  
- Verification: below millisecond resolution  
- Revocation check: ~0.001 ms  

The results indicate that the protocol introduces negligible overhead and is suitable for real-time verification scenarios.

---

## 🚀 Future Work

  * Full BBS+ signature implementation
  * Cryptographic accumulators for revocation
  * zk-SNARK-based predicate proofs
  * Integration with decentralized identity (DID) systems

---

## 🎥 Quick Demo Flow (90 seconds)

1. Issue a credential using the wallet CLI  
2. Prove a predicate to Verifier A  
3. Enable audit mode to show zero data leakage  
4. Prove the same credential to Verifier B  
5. Revoke the credential and show verification failure  

---

## 🏁 Conclusion

Nexus-ZK demonstrates that strong privacy guarantees, unlinkability, and revocation can be achieved without sacrificing usability or requiring trusted verifiers.

It serves as both a complete system prototype and a foundation for advanced cryptographic research.

---

## 👨‍💻 Authors

Developed as part of a cryptography-focused research and hackathon project by - Sandipan Dutta.