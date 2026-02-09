import json
import requests
import os

ISSUER_URL = "http://127.0.0.1:8000"
VERIFIER_URL = "http://127.0.0.1:8001"
CREDENTIAL_FILE = "wallet/credential.json"


class Wallet:
    def __init__(self):
        if not os.path.exists("wallet"):
            os.makedirs("wallet")

    def save_credential(self, credential: dict):
        with open(CREDENTIAL_FILE, "w") as f:
            json.dump(credential, f, indent=2)

    def load_credential(self) -> dict:
        if not os.path.exists(CREDENTIAL_FILE):
            raise Exception("No credential found. Issue one first.")
        with open(CREDENTIAL_FILE, "r") as f:
            return json.load(f)

    # -----------------------------
    # ISSUER INTERACTION
    # -----------------------------

    def issue_credential(self, age: int, country: str, student: bool):
        payload = {
            "age": age,
            "country": country,
            "student": student
        }
        resp = requests.post(f"{ISSUER_URL}/issue", json=payload)
        resp.raise_for_status()
        credential = resp.json()
        self.save_credential(credential)
        return credential

    # -----------------------------
    # VERIFIER INTERACTION
    # -----------------------------

    def get_nonce(self) -> str:
        resp = requests.get(f"{VERIFIER_URL}/challenge")
        resp.raise_for_status()
        return resp.json()["nonce"]

    def verify_proof(self, predicate: str):
        credential = self.load_credential()
        nonce = self.get_nonce()

        payload = {
            "credential": credential,
            "predicate": predicate,
            "nonce": nonce
        }

        resp = requests.post(f"{VERIFIER_URL}/verify", json=payload)
        resp.raise_for_status()
        return resp.json()
