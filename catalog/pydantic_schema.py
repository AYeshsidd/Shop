from pydantic import BaseModel , Field
from typing import Optional

from datetime import datetime

class Categorycreate(BaseModel):
    name: str = Field(min_length=4 , max_length=100)
    description:str 

class CategoryOut(BaseModel):
    category_id: int
    name: str
    created_at: datetime

class Config:  # convert sqlalchemy object into pydantic model
        from_attributes = True
    
class ProductCreate(BaseModel):
    category_id: int
    product_name: str = Field(min_length=2, max_length=100)
    product_description: Optional[str] = None
    price: float = Field(gt=0) # greater than
    quantity: int = Field(ge=0, default=0) # greater than or equal to
    image_url: Optional[str] = None


class ProductOut(BaseModel):
    product_id: int
    category_id: int
    product_name: str
    product_description: Optional[str]
    price: float
    quantity: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True