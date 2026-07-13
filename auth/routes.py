from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from auth.alchemy_model import Users
from auth.pydanctic_schema import UserCreate , UserResponse
from core.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(Users).filter(
        Users.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    # Create new user object
    new_user = Users(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        address=user.address,
        role=user.role,
        password_hash=hash_password(user.password)
    )

    # Save user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user