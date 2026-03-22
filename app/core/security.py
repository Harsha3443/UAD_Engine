import secrets
import string
import hashlib

def generate_api_key(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits
    return "uad_" + "".join(secrets.choice(alphabet) for _ in range(length))

def get_api_key_hash(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()

def verify_api_key(plain_api_key: str, hashed_key: str) -> bool:
    return get_api_key_hash(plain_api_key) == hashed_key