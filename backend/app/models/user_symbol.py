from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserSymbol(Base):
    __tablename__ = "user_symbols"

    id               = Column(Integer, primary_key=True, index=True)
    user_exchange_id = Column(
        Integer,
        ForeignKey("user_exchanges.id", ondelete="CASCADE"),
        nullable=False
    )
    symbol           = Column(Text, nullable=False)
    added_at         = Column(DateTime(timezone=True), server_default=func.now())

    exchange         = relationship("UserExchange", back_populates="symbols")
