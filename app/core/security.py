"""
Authentication and JWT utility functions.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def _bcrypt_check_length(password: str):
    byte_length = len(password.encode('utf-8'))
    print(f"[DEBUG] Password: {password!r}, UTF-8 byte length: {byte_length}")
    if byte_length > 72:
        raise ValueError("Password must be at most 72 bytes when encoded as UTF-8.")

def _bcrypt_truncate(password: str) -> str:
    # This function is now a no-op, but kept for compatibility
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    _bcrypt_check_length(plain_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    _bcrypt_check_length(password)
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
