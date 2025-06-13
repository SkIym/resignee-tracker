import os
from cryptography.fernet import Fernet

FERNET_KEY = os.environ.get("FERNET_KEY")
if not FERNET_KEY:
    raise Exception("FERNET_KEY environment variable not set!")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_field(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt_field(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()