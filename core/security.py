import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from core.config import settings


"""
security.py

Purpose:
- Hash plain text passwords before storing them in the database.
- Verify user passwords during login.
- Later this file will also contain JWT token functions.
"""

# Hash Password
def hash_password(password: str) -> str:
    # bcrypt works on bytes, not str — encode first
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # store as string in DB, decode back
    return hashed.decode("utf-8")

#  Verify Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

# Create Access Token
# Short-lived token (e.g. 30 min) — sent with every API request
# to prove "this user is logged in".


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Create Refresh Token
# Long-lived token (e.g. 7 days) — used ONLY to get a new access
# token once it expires. Never sent with normal API requests.

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Decode Token
# Used to verify a token and read its data back.
# Raises an error if token is invalid or expired.

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise ValueError("Invalid or expired token")