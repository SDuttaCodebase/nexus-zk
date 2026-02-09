class ProofGenerator:
    def generate_proof(self, credential, predicate, issuer=None):
        attributes = credential["payload"]["attributes"]

        if predicate == "age_over_18":
            return {"valid": attributes["age"] >= 18}

        if predicate == "is_student":
            return {"valid": attributes["student"] is True}

        return {"valid": False}
