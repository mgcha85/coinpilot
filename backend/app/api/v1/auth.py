# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/v1/auth", tags=["auth"])
security = HTTPBearer()

@router.get("/me", response_model=UserRead)
def read_current_user(
    cred: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = cred.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(UserModel).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.from_orm(user)

# 회원가입
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
) -> UserRead:
    # 중복 확인
    exists = db.query(UserModel).filter(
        (UserModel.username == payload.username) | (UserModel.email == payload.email)
    ).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    # 비밀번호 해싱
    hashed_pw = pwd_context.hash(payload.password)
    user = UserModel(
        username=payload.username,
        email=payload.email,
        hashed_password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )

# 로그인
@router.post("/login", response_model=Token)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
) -> Token:
    user = db.query(UserModel).filter(UserModel.email == credentials.email).first()
    # 이메일 또는 비밀번호 불일치
    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # JWT 생성
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user.id), "exp": expire}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=access_token, token_type="bearer")
