from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.db import get_db
from core.security import decode_token
from auth.alchemy_model import Users

"""
dependencies.py

Purpose:
- Extract the JWT access token from the request's Authorization header.
- Verify it (signature + expiry) using decode_token().
- Look up the user in the database.
- Give the current logged-in user to any route that needs it.
- check permisions for current logged-in user like he can delete/update/remove.

"""

# This tells FastAPI: "expect a simple Bearer token in the
# Authorization header — just a token, no username/password form."
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Users:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials  # raw JWT string nikal rahe hain yahan se

    try:
        payload = decode_token(token)
    except ValueError:
        raise credentials_exception

    # Make sure it's an ACCESS token, not a refresh token
    if payload.get("type") != "access":
        raise credentials_exception

    email = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = db.query(Users).filter(Users.email == email).first()
    if user is None:
        raise credentials_exception

    return user

# ROLE BASED
def require_role(*allowed_roles: str):
    def role_checker(current_user: Users = Depends(get_current_user)) -> Users:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action"
            )
        return current_user
    return role_checker