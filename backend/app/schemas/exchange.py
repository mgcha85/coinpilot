from pydantic import BaseModel, constr
from typing import List, Literal
from datetime import datetime

class ExchangeBase(BaseModel):
    service: str
    api_key: str
    secret_key: str
    market_type: Literal['spot','future','both']
    is_main: bool = False

class ExchangeCreate(ExchangeBase):
    pass

class ExchangeRead(ExchangeBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class SymbolCreate(BaseModel):
    exchange_id: int
    symbol: constr(min_length=1)

class SymbolRead(BaseModel):
    id: int
    exchange_id: int
    symbol: str
    added_at: datetime

    class Config:
        orm_mode = True

# If you’d rather keep SymbolsPayload in schemas:
class SymbolsPayload(BaseModel):
    symbols: List[str]
