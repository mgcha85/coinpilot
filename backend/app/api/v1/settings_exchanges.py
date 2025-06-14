# app/api/v1/settings_exchanges.py
from fastapi import APIRouter, Depends, HTTPException, status, Query, Security, Path, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt

from pydantic import BaseModel

from app.models.user_symbol import UserSymbol
from app.schemas.exchange import SymbolRead

from app.db.session import get_db
from app.models.user_exchange import UserExchange
from app.models.user_symbol import UserSymbol
from app.schemas.exchange import (
    ExchangeCreate, ExchangeRead,
    SymbolCreate, SymbolRead
)
from app.core.security import encrypt_text, decrypt_text
from app.config import SECRET_KEY, ALGORITHM


router = APIRouter(prefix="/v1/settings/exchanges", tags=["settings"])
security = HTTPBearer()

# 임시로 user_id를 query parameter로 받습니다.
def get_current_user_id(
    cred: HTTPAuthorizationCredentials = Security(security)
) -> int:
    token = cred.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return int(payload.get("sub"))

def get_user_id(user_id: int = Query(..., description="User ID")) -> int:
    return user_id

# 1) 사용자별 거래소 리스트 조회
@router.get("/", response_model=List[ExchangeRead])
def list_exchanges(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    objs = (
        db.query(UserExchange)
          .filter(UserExchange.user_id == user_id)
          .order_by(UserExchange.id)
          .all()
    )
    return [
        ExchangeRead(
            id=e.id,
            service=e.service,
            api_key=decrypt_text(e.api_key_enc),
            secret_key=decrypt_text(e.secret_key_enc),
            market_type=e.market_type,
            is_main=e.is_main,
            created_at=e.created_at
        ) for e in objs
    ]

# 2) 거래소 설정 생성·업데이트 (Upsert)
@router.post("/", response_model=ExchangeRead, status_code=status.HTTP_201_CREATED)
def upsert_exchange(
    payload: ExchangeCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    enc_key    = encrypt_text(payload.api_key)
    enc_secret = encrypt_text(payload.secret_key)

    if payload.is_main:
        db.query(UserExchange).filter(UserExchange.user_id == user_id).update({"is_main": False})

    obj = (
        db.query(UserExchange)
          .filter_by(user_id=user_id, service=payload.service)
          .first()
    )
    if obj:
        obj.api_key_enc    = enc_key
        obj.secret_key_enc = enc_secret
        obj.market_type    = payload.market_type
        obj.is_main        = payload.is_main
    else:
        obj = UserExchange(
            user_id=user_id,
            service=payload.service,
            api_key_enc=enc_key,
            secret_key_enc=enc_secret,
            market_type=payload.market_type,
            is_main=payload.is_main
        )
        db.add(obj)

    db.commit()
    db.refresh(obj)

    return ExchangeRead(
        id=obj.id,
        service=obj.service,
        api_key=payload.api_key,
        secret_key=payload.secret_key,
        market_type=obj.market_type,
        is_main=obj.is_main,
        created_at=obj.created_at
    )

# 3) 주 거래소 기준 심볼 리스트 조회
@router.get("/symbols", response_model=List[str])
def get_symbols(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    main = (
      db.query(UserExchange)
        .filter_by(user_id=user_id, is_main=True)
        .first()
    )
    if not main:
        raise HTTPException(status_code=404, detail="Main exchange not set")

    from app.core.fetcher import fetch_exchange_symbols
    return fetch_exchange_symbols(
        main.service, main.market_type
    )

# 4) 모니터링할 심볼 저장
@router.post("/symbols", response_model=SymbolRead, status_code=status.HTTP_201_CREATED)
def add_symbol(
    payload: SymbolCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    exch = db.query(UserExchange).filter_by(id=payload.exchange_id, user_id=user_id).first()
    if not exch:
        raise HTTPException(status_code=404, detail="Exchange not found")

    sym = UserSymbol(exchange_id=payload.exchange_id, symbol=payload.symbol)
    db.add(sym)
    db.commit()
    db.refresh(sym)
    return sym


@router.put(
    "/{exchange_id}",
    response_model=ExchangeRead,
    status_code=status.HTTP_200_OK,
)
def update_exchange(
    exchange_id: int = Path(..., description="Exchange ID"),
    payload: ExchangeCreate = Body(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    obj = db.query(UserExchange).filter_by(id=exchange_id, user_id=user_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Exchange not found")

    # 주거래소 플래그 관리
    if payload.is_main:
        db.query(UserExchange).filter(UserExchange.user_id == user_id).update({"is_main": False})

    # 업데이트
    obj.service        = payload.service
    obj.api_key_enc    = encrypt_text(payload.api_key)
    obj.secret_key_enc = encrypt_text(payload.secret_key)
    obj.market_type    = payload.market_type
    obj.is_main        = payload.is_main

    db.commit()
    db.refresh(obj)
    return ExchangeRead.from_orm(obj)


# b1) 심볼 전체 조회(GET)
@router.get(
    "/{exchange_id}/symbols/",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
)
def get_symbols_by_exchange(
    exchange_id: int = Path(..., description="Exchange ID"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    exch = db.query(UserExchange).filter_by(id=exchange_id, user_id=user_id).first()
    if not exch:
        raise HTTPException(status_code=404, detail="Exchange not found")

    from app.core.fetcher import fetch_exchange_symbols
    return fetch_exchange_symbols(exch.service, exch.market_type)


# b2) 심볼 일괄 저장(PUT)
class SymbolsPayload(BaseModel):
    symbols: List[str]

@router.put(
    "/{exchange_id}/symbols/",
    response_model=List[SymbolRead],
    status_code=status.HTTP_200_OK,
)
def replace_symbols(
    exchange_id: int = Path(..., description="Exchange ID"),
    payload: SymbolsPayload = Body(...),       # Body(...) 로 기본값 할당
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    exch = db.query(UserExchange).filter_by(id=exchange_id, user_id=user_id).first()
    if not exch:
        raise HTTPException(status_code=404, detail="Exchange not found")

    # 기존 심볼 전부 삭제
    db.query(UserSymbol).filter_by(user_exchange_id=exchange_id).delete()

    # 새로 삽입
    objs = []
    for sym in payload.symbols:
        obj = UserSymbol(exchange_id=exchange_id, symbol=sym)
        db.add(obj)
        objs.append(obj)
    db.commit()
    return objs