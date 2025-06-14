from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
# 기존 User 클래스에 이어서…


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    exchanges = relationship("UserExchange", back_populates="user", cascade="all, delete-orphan")
