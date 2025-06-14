# app/config.py
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# JWT 서명에 사용할 비밀 키
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-if-not-set")

# 사용할 알고리즘 (HS256, HS512 등)
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# 토큰 만료 시간 등 다른 설정도 여기에 추가할 수 있습니다.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
