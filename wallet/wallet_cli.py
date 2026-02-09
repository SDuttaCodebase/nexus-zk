import sys
from wallet.wallet import Wallet

wallet = Wallet()

def usage():
    print("Usage:")
    print("  python wallet/wallet_cli.py issue")
    print("  python wallet/wallet_cli.py prove <predicate>")
    sys.exit(1)


if len(sys.argv) < 2:
    usage()

command = sys.argv[1]

if command == "issue":
    print("Issuing credential...")
    cred = wallet.issue_credential(
        age=21,
        country="India",
        student=True
    )
    print("Credential stored locally.")
    print("Revocation hash:", cred["payload"]["revocation_hash"])

elif command == "prove":
    if len(sys.argv) != 3:
        usage()
    predicate = sys.argv[2]
    print(f"Proving predicate: {predicate}")
    result = wallet.verify_proof(predicate)
    print("Verifier response:", result)

else:
    usage()
