from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

class BBSSignature:
    def __init__(self):
        self.sk = Ed25519PrivateKey.generate()
        self.pk = self.sk.public_key()

    def sign(self, message: bytes) -> bytes:
        return self.sk.sign(message)

    def verify(self, message: bytes, signature: bytes) -> bool:
        try:
            self.pk.verify(signature, message)
            return True
        except:
            return False
