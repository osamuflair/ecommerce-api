from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserResponse
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token
DUMMY_PASSWORD = hash_password("DummY_PAsswORD123#$%")

def authenticate_user(db: Session, username: str, password: str) -> UserResponse:
    existing_user = db.query(User).filter(User.username == username).first()
    if not existing_user:
        verify_password(password, DUMMY_PASSWORD)
        raise HTTPException(status_code = 401, detail = "invalid username or password")
    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code = 401, detail = "invalid username or password")
    return existing_user

def log_in(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if user.is_active is False:
        raise HTTPException(status_code = 403, detail = "Forbidden, Account is Deactivated")
    return create_access_token(data={"sub": user.username})