from fastapi import FastAPI
from pydantic import BaseModel
import json

from issuer.issuer import Issuer
from services.issuer_api.storage import init_db, get_connection

app = FastAPI(title="Nexus-ZK Issuer Service")

issuer = Issuer()
init_db()

# -----------------------------
# Request / Response Schemas
# -----------------------------

class IssueRequest(BaseModel):
    age: int
    country: str
    student: bool


class RevokeRequest(BaseModel):
    revocation_hash: str


# -----------------------------
# API Endpoints
# -----------------------------

@app.post("/issue")
def issue_credential(req: IssueRequest):
    credential = issuer.issue_credential(req.dict())

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO credentials (payload, signature, revocation_hash) VALUES (?, ?, ?)",
        (
            json.dumps(credential["payload"]),
            credential["signature"].hex(),
            credential["payload"]["revocation_hash"]
        )
    )
    conn.commit()
    conn.close()

    # ✅ JSON-safe response
    return {
        "payload": credential["payload"],
        "signature": credential["signature"].hex(),
        "revocation_secret": credential["revocation_secret"]
    }



@app.post("/revoke")
def revoke_credential(req: RevokeRequest):
    issuer.revoke(req.revocation_hash)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO revocations (revocation_hash) VALUES (?)",
        (req.revocation_hash,)
    )
    conn.commit()
    conn.close()

    return {"status": "revoked", "revocation_hash": req.revocation_hash}

@app.get("/is_revoked/{revocation_hash}")
def is_revoked(revocation_hash: str):
    return {
        "revoked": revocation_hash in issuer.revocation_registry
    }
