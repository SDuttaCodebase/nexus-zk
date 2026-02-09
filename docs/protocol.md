# Nexus-ZK Protocol Specification

## 1. Overview

Nexus-ZK is a privacy-preserving, multi-verifier credential system that allows a user (holder) to prove selected attributes or predicates about themselves to multiple independent verifiers without revealing the underlying attributes and without allowing linkage across verifications.

The system is designed to satisfy the goals of:
- Selective disclosure
- Non-linkability across verifiers
- Revocable credentials
- Minimal trust assumptions

---

## 2. System Roles

### 2.1 Issuer
The Issuer is a trusted authority (e.g., university, government body) responsible for issuing credentials to users.  
The Issuer:
- Signs user attributes
- Maintains a revocation registry
- Does NOT track how or where credentials are used

### 2.2 Holder
The Holder is the user who receives a credential and stores it in a wallet.  
The Holder:
- Generates zero-knowledge proofs for specific predicates
- Creates verifier-specific pseudonyms
- Keeps revocation secrets private

### 2.3 Verifier
A Verifier is any independent system that needs to verify a claim about a user.  
The Verifier:
- Receives only a proof (true/false)
- Learns no identifying information
- Cannot link multiple sessions

---

## 3. Credential Structure

Each issued credential contains:

- User attributes (e.g., age, country, student status)
- A revocation hash
- A cryptographic signature from the issuer
- A secret revocation token (known only to the holder)

The issuer never stores the revocation secret.

---

## 4. Protocol Flow

### Step 1: Credential Issuance
1. The Holder submits attributes to the Issuer.
2. The Issuer generates a revocation secret and corresponding hash.
3. The Issuer signs the credential payload.
4. The credential is returned to the Holder.

---

### Step 2: Proof Generation
1. The Holder selects a predicate (e.g., age ≥ 18).
2. The Holder generates a zero-knowledge proof that:
   - The predicate is satisfied
   - The credential is not revoked
3. No raw attribute values are disclosed.

---

### Step 3: Verification
1. The Verifier receives the proof.
2. The Verifier checks proof validity.
3. The Verifier outputs only accept/reject.

---

### Step 4: Revocation
1. The Issuer adds a revocation hash to the revocation registry.
2. Future proofs referencing this credential fail.
3. Revocation does not reveal user identity or enable linkage.

---

## 5. Design Goals

- Privacy by default
- Minimal disclosure
- Resistance to verifier collusion
- Simple and auditable implementation

---

## 6. Extensibility

The protocol is designed to be extensible to:
- BBS+ signatures with full selective disclosure
- Cryptographic accumulators
- zk-SNARK-based predicate proofs

These extensions are left as future work.
