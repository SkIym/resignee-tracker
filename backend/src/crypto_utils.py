from cryptography.fernet import Fernet
import os

# You should store this key securely!
FERNET_KEY = os.environ.get("FERNET_KEY", Fernet.generate_key())
fernet = Fernet(FERNET_KEY)

def encrypt_field(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt_field(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()