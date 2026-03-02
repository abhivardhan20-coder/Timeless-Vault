from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(key)

def encrypt_data(data: bytes) -> str:
    return cipher.encrypt(data).decode()

def decrypt_data(token: str) -> bytes:
    return cipher.decrypt(token.encode())