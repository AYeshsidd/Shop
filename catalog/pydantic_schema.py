from pydantic import BaseModel , Field , Optional
from typing import Literal
from datetime import datetime

class Categorycreate(BaseModel):
    name: str = Field(min_length=4 , max_length=100)
    description: Optional[str] = None

class CategoryOut(BaseModel):
    category_id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:  # convert sqlalchemy object into pydantic model
        from_attributes = True
    

class ProductCreate(BaseModel):
    category_id: int
    product_name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    price: float = Field(gt=0) # greater than
    quantity: int = Field(ge=0, default=0) #greater than or equal to
    image_url: Optional[str] = None


class ProductOut(BaseModel):
    product_id: int
    category_id: int
    product_name: str
    description: Optional[str]
    price: float
    quantity: int
    image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True