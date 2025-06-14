from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.api_key import APIKey as APIKeyModel
from app.schemas.api_key import APIKeyCreate, APIKeyRead
from app.core.security import encrypt_text, decrypt_text

router = APIRouter(prefix="/v1/settings/api-keys", tags=["settings"])

@router.post("/", response_model=APIKeyRead, status_code=status.HTTP_201_CREATED)
def create_api_key(
    payload: APIKeyCreate,
    db: Session = Depends(get_db),
) -> APIKeyRead:
    api_enc = encrypt_text(payload.api_key)
    secret_enc = encrypt_text(payload.secret_key)

    db_obj = APIKeyModel(
        user_id=payload.user_id,
        service=payload.service,
        api_key_enc=api_enc,
        secret_key_enc=secret_enc,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return APIKeyRead(
        id=db_obj.id,
        service=db_obj.service,
        api_key=decrypt_text(db_obj.api_key_enc),
        secret_key=decrypt_text(db_obj.secret_key_enc),
        created_at=db_obj.created_at,
    )

@router.get("/", response_model=List[APIKeyRead])
def list_api_keys(
    db: Session = Depends(get_db),
) -> List[APIKeyRead]:
    objs = db.query(APIKeyModel).order_by(APIKeyModel.id.desc()).all()
    return [
        APIKeyRead(
            id=obj.id,
            service=obj.service,
            api_key=decrypt_text(obj.api_key_enc),
            secret_key=decrypt_text(obj.secret_key_enc),
            created_at=obj.created_at,
        )
        for obj in objs
    ]
