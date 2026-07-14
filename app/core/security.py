from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.config import settings
from app.models.user import User, UserRole

password_hash = PasswordHash.recommended()

WAT = timezone(timedelta(hours=1))

def hash_password(password):
    """Hashes a password."""
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    """Verifies a password with its hashed password."""
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates access token for a current user."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(WAT) + expires_delta
    else:
        expire = datetime.now(WAT) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    jwt_encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encoded

def decode_token(token):
    """Decodes access token"""
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded.get('sub')
    except jwt.PyJWTError:
        return None
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_session)):
    """
    Gives access to a valid user.
    
    Decodes the access token of the user.
    Validates that the username gotten from the token exists.

    Args:
        token: JWT access token extracted from the Authorization header.
        db: DB session.

    Returns:
        The authenticated User object.

    Raises:
        HTTPException 401: If token is invalid or user is not found.
    """
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    from app.services.user_service import get_user_by_username
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_staff(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Gives access to staff and admin."""
    if current_user.role not in (UserRole.STAFF, UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Staff access required")
    return current_user

def require_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Gives access to admin only."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user