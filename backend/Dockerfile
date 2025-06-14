# backend/Dockerfile

# 1) 베이스 이미지
FROM python:3.11-slim

# 2) 작업 디렉터리
WORKDIR /usr/src/app

# 3) 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) 앱 소스 복사
COPY . .

# 5) 빌드 아규먼트로 DATABASE_URL 주입
ARG DATABASE_URL
ENV DATABASE_URL=${DATABASE_URL}

# 7) 컨테이너 시작 명령
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
