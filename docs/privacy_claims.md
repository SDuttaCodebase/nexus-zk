# Privacy Claims of Nexus-ZK

## 1. Overview

This document formally states the privacy guarantees provided by the Nexus-ZK system under the threat model defined in `threat_model.md`.

All claims assume standard cryptographic hardness assumptions and correct protocol execution.

---

## 2. Selective Disclosure

**Claim:**  
The holder can prove a predicate about an attribute without revealing the attribute value itself.

**Justification:**  
Proofs operate on predicates (e.g., age ≥ 18) rather than raw attributes. Verifiers receive only a boolean outcome.

---

## 3. Unlinkability Across Verifiers

**Claim:**  
Two or more verifiers cannot determine whether proofs originate from the same holder.

**Justification:**  
Verifier-specific pseudonyms are derived using secret holder data combined with verifier identifiers. No global identifier is reused across verification contexts.

---

## 4. Session Unlinkability

**Claim:**  
Multiple proof sessions with the same verifier cannot be linked to the same holder.

**Justification:**  
Proofs do not include stable identifiers and can be extended with session-specific randomness or nonces.

---

## 5. Issuer Unlinkability

**Claim:**  
The issuer cannot determine where, when, or how a credential is used.

**Justification:**  
The issuer is not involved in proof generation or verification and does not receive proof transcripts.

---

## 6. Privacy-Preserving Revocation

**Claim:**  
Credential revocation does not reveal the identity of the holder and does not enable proof linkage.

**Justification:**  
Revocation is performed using hashed revocation tokens. The revocation secret is never disclosed, and revocation checks reveal only validity status.

---

## 7. Minimal Disclosure Principle

**Claim:**  
No party learns more information than strictly required for verification.

**Justification:**  
Verifiers learn only proof validity. Issuers learn only issuance and revocation events. No additional metadata is shared.

---

## 8. Limitations

The following are explicitly not guaranteed:
- Anonymity against device compromise
- Resistance to global side-channel attacks
- Protection against compromised cryptographic primitives

---

## 9. Privacy Summary

Nexus-ZK provides strong practical privacy guarantees including:
- Selective disclosure
- Unlinkability across verifiers
- Unlinkable revocation
- Issuer blindness to credential usage

These guarantees are achieved without requiring trusted verifiers or shared global identifiers.
