from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from fastapi import HTTPException
from app.core.security import hash_password

def create_user(db: Session, user_data: UserCreate) -> User:
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
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if updated_data.username:
        user.username = updated_data.username
    if updated_data.email:
        user.email = updated_data.email
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def deactivate_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user