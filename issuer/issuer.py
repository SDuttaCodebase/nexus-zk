import os
import hashlib
import json
from crypto.bbs import BBSSignature

class Issuer:
    def __init__(self):
        self.bbs = BBSSignature()
        self.revocation_registry = set()  # stores revoked hashes

    def issue_credential(self, attributes: dict):
        revocation_secret = os.urandom(32).hex()
        revocation_hash = hashlib.sha256(revocation_secret.encode()).hexdigest()

        payload = {
            "attributes": attributes,
            "revocation_hash": revocation_hash
        }

        signature = self.bbs.sign(json.dumps(payload).encode())

        return {
            "payload": payload,
            "signature": signature,
            "revocation_secret": revocation_secret
        }

    def revoke(self, revocation_hash: str):
        self.revocation_registry.add(revocation_hash)
