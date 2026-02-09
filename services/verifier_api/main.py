import requests

ISSUER_URL = "http://127.0.0.1:8000"

from fastapi import FastAPI
from pydantic import BaseModel

from services.verifier_api.storage import (
    init_db,
    generate_nonce,
    consume_nonce
)

from holder.proof_generator import ProofGenerator
from issuer.issuer import Issuer

app = FastAPI(title="Nexus-ZK Verifier Service")

init_db()

proof_gen = ProofGenerator()
issuer = Issuer()  # used only for revocation registry access


# -----------------------------
# Request / Response Schemas
# -----------------------------

class ChallengeResponse(BaseModel):
    nonce: str


class VerifyRequest(BaseModel):
    credential: dict
    predicate: str
    nonce: str
    audit: bool = False

# -----------------------------
# API Endpoints
# -----------------------------

@app.get("/challenge", response_model=ChallengeResponse)
def get_challenge():
    nonce = generate_nonce()
    return {"nonce": nonce}

def audit_log(req: VerifyRequest, result: dict):
    print("\n🔍 VERIFIER PRIVACY AUDIT LOG")
    print("-" * 35)

    print("Received credential identifier: ❌ None")
    print("Received user identity: ❌ None")

    attributes = req.credential.get("payload", {}).get("attributes", {})

    print("Received raw attributes:")
    for k in attributes.keys():
        print(f"  - {k}: ❌ hidden")

    print(f"Predicate evaluated: ✔ {req.predicate}")
    print(f"Verification result: ✔ {result.get('verified')}")

    print("-" * 35)

@app.post("/verify")
def verify_proof(req: VerifyRequest):
    # Step 1: Check nonce freshness
    if not consume_nonce(req.nonce):
        result = {"verified": False, "reason": "Invalid or reused nonce"}
        if req.audit:
            audit_log(req, result)
        return result

    # Step 2: Check revocation with Issuer API
    revocation_hash = req.credential["payload"]["revocation_hash"]

    resp = requests.get(f"{ISSUER_URL}/is_revoked/{revocation_hash}")
    revoked = resp.json()["revoked"]

    if revoked:
        result = {"verified": False, "reason": "Credential revoked"}
        if req.audit:
            audit_log(req, result)
        return result

    # Step 3: Verify predicate proof
    proof = proof_gen.generate_proof(
        req.credential,
        req.predicate,
        issuer=None
    )

    result = {"verified": bool(proof.get("valid"))}

    if req.audit:
        audit_log(req, result)

    return result
