import time
from issuer.issuer import Issuer
from holder.wallet import Wallet
from holder.proof_generator import ProofGenerator
from verifier.verifier_a import verify as verify_a

ITERATIONS = 1000

def benchmark_issue():
    issuer = Issuer()
    start = time.time()
    for _ in range(ITERATIONS):
        issuer.issue_credential({
            "age": 21,
            "country": "India",
            "student": True
        })
    end = time.time()
    return (end - start) / ITERATIONS * 1000  # ms


def benchmark_proof_generation():
    issuer = Issuer()
    credential = issuer.issue_credential({
        "age": 21,
        "country": "India",
        "student": True
    })
    proof_gen = ProofGenerator()

    start = time.time()
    for _ in range(ITERATIONS):
        proof_gen.generate_proof(credential, "age_over_18", issuer)
    end = time.time()
    return (end - start) / ITERATIONS * 1000


def benchmark_verification():
    issuer = Issuer()
    credential = issuer.issue_credential({
        "age": 21,
        "country": "India",
        "student": True
    })
    proof_gen = ProofGenerator()
    proof = proof_gen.generate_proof(credential, "age_over_18", issuer)

    start = time.time()
    for _ in range(ITERATIONS):
        verify_a(proof)
    end = time.time()
    return (end - start) / ITERATIONS * 1000


def benchmark_revocation_check():
    issuer = Issuer()
    credential = issuer.issue_credential({
        "age": 21,
        "country": "India",
        "student": True
    })
    proof_gen = ProofGenerator()

    issuer.revoke(credential["payload"]["revocation_hash"])

    start = time.time()
    for _ in range(ITERATIONS):
        proof_gen.generate_proof(credential, "age_over_18", issuer)
    end = time.time()
    return (end - start) / ITERATIONS * 1000


if __name__ == "__main__":
    print("Average Credential Issuance Time (ms):", round(benchmark_issue(), 4))
    print("Average Proof Generation Time (ms):", round(benchmark_proof_generation(), 4))
    print("Average Verification Time (ms):", round(benchmark_verification(), 4))
    print("Average Revocation Check Time (ms):", round(benchmark_revocation_check(), 4))
