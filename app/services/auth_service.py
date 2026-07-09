from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException
from app.core.security import hash_password, verify_password, create_access_token
DUMMY_PASSWORD = hash_password("DummY_PAsswORD123#$%")

def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Authenticate a user.
    
    Validates that the user exists.
    Validates that the entered password is the correct password.
    Validates the entered password against a dummy password if the user does not exists.

    Args:
        db: DB session.
        username: username entered by user.
        password: password entered by user.

    Returns:
        The User object.

    Raises:
        HTTPException 401: If user does not exists, or a wrong password was entered.
    """
    existing_user = db.query(User).filter(User.username == username).first()
    if not existing_user:
        verify_password(password, DUMMY_PASSWORD)
        raise HTTPException(status_code = 401, detail = "invalid username or password")
    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code = 401, detail = "invalid username or password")
    return existing_user

def log_in(db: Session, username: str, password: str) -> str:
    """
    Logs in a user.
    
    Validates the credentials entered by the user, using authenticate_user.
    Validates that the user account is not deactivated, using user.is_active.
    Creates an access token for the user

    Args:
        db: DB session.
        username: username entered by user.
        password: password entered by user.

    Returns:
        Access token.

    Raises:
        HTTPException 403: If users account is deactivated
    """
    user = authenticate_user(db, username, password)
    if user.is_active is False:
        raise HTTPException(status_code = 403, detail = "Forbidden, Account is Deactivated")
    return create_access_token(data={"sub": user.username})