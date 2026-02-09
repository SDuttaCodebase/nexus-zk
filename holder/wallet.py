import hashlib
import json

class Wallet:
    def __init__(self, credential):
        self.credential = credential

    def get_revocation_hash(self):
        secret = self.credential["revocation_secret"]
        return hashlib.sha256(secret.encode()).hexdigest()

    def create_pseudonym(self, verifier_id: str):
        base = self.credential["revocation_secret"] + verifier_id
        return hashlib.sha256(base.encode()).hexdigest()
