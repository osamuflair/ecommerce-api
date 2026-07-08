from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from fastapi import HTTPException
from app.core.security import hash_password

def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Creates a new user account along with a default cart and wishlist.

    Validates that the username and email are not already in use.
    Creates the user, along with the cart and wishlist.

    Args:
        db: Database session.
        user_data: UserCreate model that contains the username and email of the user

    Returns:
        The newly created User object.

    Raises:
        HTTPException 400: If username or email already exists.
    """
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_username:
        raise HTTPException(status_code = 400, detail = "username already taken")
    if existing_email:
        raise HTTPException(status_code = 400, detail = "email address already in use")
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hash_password(user_data.password)
    )
    db.add(new_user)
    db.flush()

    new_cart = Cart(user_id = new_user.id)
    new_wishlist = Wishlist(user_id = new_user.id)
    db.add(new_cart)
    db.add(new_wishlist)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, updated_data: UserUpdate) -> User:
    """
    Updates the current user's username and/or email.

    Validates that the current user exists.
    Validates that the username and/or email are not already in use by other users but the current user.
    Updates the current user.

    Args:
        db: Database session.
        user_id: ID of the current user.
        updated_data: UserUpdate model that contains the username and email the user wants to change to.

    Returns:
        The updated User object.

    Raises:
        HTTPException 400: If username or email already exists.
        HTTPException 404: If user does not exists.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_data.username:
        existing_username = db.query(User).filter(User.username == updated_data.username).first()
        if existing_username and existing_username.id != user.id:
            raise HTTPException(status_code = 400, detail = "username already taken")
        user.username = updated_data.username
    if updated_data.email: 
        existing_email = db.query(User).filter(User.email == updated_data.email).first()
        if existing_email and existing_email.email != user.email:
            raise HTTPException(status_code = 400, detail = "email address already in use")
        user.email = updated_data.email
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str) -> User | None:
    """Returns the User object for a particular username or None if the username is not found"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Returns the User object for a particular user id or None if the user id is not found"""
    return db.query(User).filter(User.id == user_id).first()

def deactivate_user(db: Session, user_id: int) -> User:
    """
    Deactivates the current user's account by setting is_active to False.

    Validates that the user exists.
    Deactivates the user.

    Args:
        db: Database session.
        user_id: ID of the current user.

    Returns:
        The deactivated User object.

    Raises:
        HTTPException 404: If user does not exists.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user