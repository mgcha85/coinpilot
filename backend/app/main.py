from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.settings import router as settings_router
from app.api.v1.settings_exchanges import router as settings_exchanges_router
from app.api.v1.rs import router as rs_router
from app.api.v1.auth import router as auth_router

app = FastAPI()

# 허용할 도메인 리스트
origins = [
    "http://localhost:3000",
    # 배포 시 실제 도메인도 여기에 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 허용 도메인
    allow_credentials=True,
    allow_methods=["*"],              # 허용 메소드
    allow_headers=["*"],              # 허용 헤더
)

app.include_router(settings_router)
app.include_router(rs_router)
app.include_router(auth_router)
app.include_router(settings_exchanges_router)
