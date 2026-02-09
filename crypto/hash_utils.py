import hashlib

def hash_to_int(data: str) -> int:
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)
