# app/core/security.py
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# .env 에서 FERNET_KEY를 읽어오도록 미리 로드
load_dotenv()

def _get_key():
    # 이 시점에는 반드시 .env의 FERNET_KEY가 들어와 있어야 합니다.
    key = os.getenv("FERNET_KEY")
    if not key:
        # 개발 중 실수 방지용 예비 처리
        key = Fernet.generate_key().decode()
        os.environ["FERNET_KEY"] = key
    return key.encode()

fernet = Fernet(_get_key())

def encrypt_text(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
