from sqlalchemy import Column , String , Integer, DateTime , DECIMAL , ForeignKey , func
from sqlalchemy.orm import relationship
from core.db import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    products = relationship("Product", back_populates="category")

    
class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    product_name = Column(String(120), nullable=False)
    product_description = Column(String(120), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="products")
