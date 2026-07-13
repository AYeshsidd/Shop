from datetime import datetime
from pydantic import BaseModel , Field , field_validator
from typing import Literal

class UserCreate(BaseModel):
    full_name : str
    email : str
    role : Literal["customer", "admin", "cashier"] = "customer"
    phone : str
    address : str
    password: str = Field(min_length=8, max_length=72)

    @field_validator('role',mode="before")
    @classmethod
    def normalize_role(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value
    

class Userlogin(BaseModel):
    email : str
    password: str = Field(min_length=8, max_length=72)
    role : Literal["customer", "admin", "cashier"] = "customer"
    phone : str



class UserResponse(BaseModel):
        user_id: int
        full_name: str
        email: str
        phone: str
        address: str
        role: str
        created_at:datetime

        class Config:
            from_attributes = True
    
