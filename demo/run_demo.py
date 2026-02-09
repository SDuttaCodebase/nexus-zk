from issuer.issuer import Issuer
from holder.wallet import Wallet
from holder.proof_generator import ProofGenerator
from verifier.verifier_a import verify as verify_a
from verifier.verifier_b import verify as verify_b

issuer = Issuer()

credential = issuer.issue_credential({
    "age": 21,
    "country": "India",
    "student": True
})

wallet = Wallet(credential)
proof_gen = ProofGenerator()

# Before revocation
proof1 = proof_gen.generate_proof(credential, "age_over_18", issuer)
print("Verifier A (before revoke):", verify_a(proof1))

# Revoke credential
issuer.revoke(credential["payload"]["revocation_hash"])

# After revocation
proof2 = proof_gen.generate_proof(credential, "is_student", issuer)
print("Verifier B (after revoke):", verify_b(proof2))
