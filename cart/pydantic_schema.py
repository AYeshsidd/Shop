from pydantic import BaseModel, Field
from datetime import datetime


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, default=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


class CartItemOut(BaseModel):
    cart_item_id: int
    product_id: int
    quantity: int
    product_name: str
    price: float
    subtotal: float

    class Config:
        from_attributes = True