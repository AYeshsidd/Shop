from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from auth.alchemy_model import Users
from auth.pydanctic_schema import UserCreate , UserResponse
from core.security import hash_password ,decode_token
from core.security import verify_password, create_access_token, create_refresh_token
from auth.pydanctic_schema import UserLogin, TokenPair , TokenRefreshRequest
from auth.dependencies import get_current_user
from auth.alchemy_model import Users


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


@router.post("/login", response_model=TokenPair)
def login(credentials: UserLogin, db: Session = Depends(get_db)):

    user = db.query(Users).filter(Users.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    token_data = {
        "sub": user.email,
        "user_id": user.user_id,
        "role": user.role
    }

    return TokenPair(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data)
    )


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: Users = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: TokenRefreshRequest, db: Session = Depends(get_db)):

    try:
        data = decode_token(payload.refresh_token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Make sure it's actually a REFRESH token, not an access token
    if data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    email = data.get("sub")
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")

    token_data = {
        "sub": user.email,
        "user_id": user.user_id,
        "role": user.role
    }

    return TokenPair(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data)
    )