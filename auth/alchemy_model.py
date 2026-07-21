from sqlalchemy import Column, Integer, String , DateTime , Enum ,func
from core.db import Base

class Users(Base): # Base will tell this belong to sql alchemy
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False , unique=True)
    role = Column(Enum("admin","customer"), default="customer", nullable=False)
    phone = Column(String(20), nullable=False , unique=True)
    address = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())