from sqlalchemy.orm import Session
from app.models.cart import CartItem, Cart
from app.schemas.cart import CartItemCreate, CartItemUpdate
from fastapi import HTTPException

def add_cart_item(db: Session, created_cart_item: CartItemCreate, cart_id: int) -> CartItem:
    existing_cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart_id,
        CartItem.product_id == created_cart_item.product_id
    ).first()
    if existing_cart_item:
        existing_cart_item.quantity += created_cart_item.quantity
        db.commit()
        db.refresh(existing_cart_item)
        return existing_cart_item
    new_cart_item = CartItem(
        cart_id = cart_id,
        product_id = created_cart_item.product_id,
        quantity = created_cart_item.quantity
    )
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    return new_cart_item

def update_cart_item(db: Session, cart_id: int, updated_cart_item: CartItemUpdate, cart_item_id: int) -> CartItem:
    existing_cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.cart_id == cart_id
    ).first()
    if not existing_cart_item:
        raise HTTPException(status_code = 404, detail = "cart item not found")
    existing_cart_item.quantity = updated_cart_item.quantity
    db.commit()
    db.refresh(existing_cart_item)
    return existing_cart_item

def remove_cart_item(db: Session, cart_id: int, cart_item_id: int) -> CartItem:
    existing_cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.cart_id == cart_id
    ).first()
    if not existing_cart_item:
        raise HTTPException(status_code = 404, detail = "cart item not found")
    db.delete(existing_cart_item)
    db.commit()
    return existing_cart_item

def get_cart_items(db: Session, cart_id: int) -> list[CartItem]:
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

def clear_cart(db: Session, cart_id: int):
    db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    db.commit()

def get_or_create_cart(db: Session, user_id: int) -> Cart:
    existing_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not existing_cart:
        new_cart = Cart(user_id = user_id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        return new_cart
    return existing_cart