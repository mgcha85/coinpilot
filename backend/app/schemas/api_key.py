from datetime import datetime
from pydantic import BaseModel

class APIKeyCreate(BaseModel):
    user_id: int
    service: str
    api_key: str
    secret_key: str

class APIKeyRead(BaseModel):
    id: int
    user_id: int
    service: str
    api_key: str
    secret_key: str
    created_at: datetime

    class Config:
        orm_mode = True
