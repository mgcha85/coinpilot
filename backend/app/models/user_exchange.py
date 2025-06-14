from sqlalchemy import (
    Column, Integer, Text, Boolean, DateTime, ForeignKey, CheckConstraint, func
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserExchange(Base):
    __tablename__ = "user_exchanges"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    service        = Column(Text, nullable=False)
    api_key_enc    = Column(Text, nullable=False)
    secret_key_enc = Column(Text, nullable=False)
    market_type    = Column(Text, nullable=False)
    is_main        = Column(Boolean, nullable=False, default=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("market_type IN ('spot','future','both')", name="chk_market_type"),
    )

    user           = relationship("User", back_populates="exchanges")
    symbols        = relationship("UserSymbol", back_populates="exchange", cascade="all, delete-orphan")
