"""
security.py

Purpose:
- Hash plain text passwords before storing them in the database.
- Verify user passwords during login.
- Later this file will also contain JWT token functions.
"""

import bcrypt

# ------------------------------------------------------------------
# Hash Password
# ------------------------------------------------------------------
def hash_password(password: str) -> str:
    # bcrypt works on bytes, not str — encode first
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # store as string in DB, decode back
    return hashed.decode("utf-8")


# ------------------------------------------------------------------
# Verify Password
# ------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )