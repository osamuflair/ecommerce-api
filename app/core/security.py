from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import settings

password_hash = PasswordHash.recommended()

WAT = timezone(timedelta(hours=1))

def hash_password(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(WAT) + expires_delta
    else:
        expire = datetime.now(WAT) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    jwt_encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encoded

def decode_token(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded.get('sub')
    except jwt.PyJWTError:
        return None