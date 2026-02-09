# Threat Model for Nexus-ZK

## 1. Overview

This document defines the adversarial assumptions and security boundaries of the Nexus-ZK system.  
The threat model follows standard cryptographic practice and assumes realistic, non-omniscient adversaries.

---

## 2. Trust Assumptions

### 2.1 Issuer Trust Model
The Issuer is assumed to be:
- Honest-but-curious
- Correctly executes the credential issuance protocol
- Does not intentionally issue malformed credentials

However, the Issuer:
- May attempt to infer user behavior
- May try to correlate issued credentials with verification events

The protocol is designed to prevent such tracking.

---

### 2.2 Holder Trust Model
The Holder may be:
- Honest
- Curious
- Potentially malicious (e.g., attempting to forge proofs)

The system ensures that:
- Invalid proofs are rejected
- Revoked credentials cannot be used successfully

---

### 2.3 Verifier Trust Model
Verifiers are assumed to be:
- Curious
- Possibly colluding with other verifiers
- Possibly colluding with the Issuer

Verifiers are not trusted with user privacy.

---

## 3. Adversary Capabilities

An adversary may:
- Observe multiple verification sessions
- Store transcripts of proofs
- Attempt to link multiple proofs to the same user
- Attempt to infer attributes beyond the proven predicate
- Attempt replay attacks

An adversary may NOT:
- Break standard cryptographic hash functions
- Forge digital signatures
- Guess high-entropy secrets

---

## 4. Threats and Mitigations

### 4.1 Verifier Linking Attacks
**Threat:**  
Multiple verifiers attempt to correlate proofs to identify the same user.

**Mitigation:**  
Verifier-specific pseudonyms are derived using secret holder data and verifier identifiers, ensuring unlinkability across verifiers.

---

### 4.2 Issuer Tracking Attacks
**Threat:**  
The issuer attempts to track where and when a credential is used.

**Mitigation:**  
The issuer never participates in proof generation or verification and does not receive proof transcripts.

---

### 4.3 Revocation-Based Identification
**Threat:**  
Revocation could reveal user identity or enable correlation.

**Mitigation:**  
Only hashed revocation tokens are stored. Revocation checks do not reveal the revocation secret or user identity.

---

### 4.4 Proof Forgery
**Threat:**  
A malicious holder attempts to generate false proofs.

**Mitigation:**  
Proof verification enforces predicate correctness and signature validity.

---

### 4.5 Replay Attacks
**Threat:**  
An attacker replays an old valid proof.

**Mitigation:**  
Proofs are verifier-context specific and can be extended with nonces or timestamps.

---

## 5. Out-of-Scope Threats

The following are considered out of scope:
- Compromise of the holder’s device
- Side-channel attacks
- Cryptographic primitive failures
- Denial-of-service attacks

---

## 6. Security Summary

Under the defined threat model, Nexus-ZK provides:
- Resistance to verifier collusion
- Protection against issuer tracking
- Unlinkable revocation
- Predicate privacy

The system achieves these guarantees without requiring a trusted verifier or shared state.
