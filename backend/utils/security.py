import hashlib, os
from typing import Tuple

def hash_password(password: str, salt: bytes | None = None
                 ) -> Tuple[bytes, bytes]:
    """
    Retorna (salt, hash) usando PBKDF2-HMAC-SHA256.
    """
    if salt is None:
        salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100_000
    )
    return salt, pwd_hash

def verify_password(password: str, salt: bytes, pwd_hash: bytes) -> bool:
    test_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100_000
    )
    return test_hash == pwd_hash
