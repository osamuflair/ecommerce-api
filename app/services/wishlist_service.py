from sqlalchemy.orm import Session
from app.models.wishlist import WishlistItem
from fastapi import HTTPException

def add_to_wishlist(db: Session, wishlist_id: int, product_id: int) -> WishlistItem:
    existing_wishlist_item = db.query(WishlistItem).filter(
        WishlistItem.wishlist_id == wishlist_id,
        WishlistItem.product_id == product_id
    ).first()
    if existing_wishlist_item:
        raise HTTPException(status_code = 400, detail = "Item already in wishlist")
    new_wishlist_item = WishlistItem(
        wishlist_id = wishlist_id,
        product_id = product_id
    )
    db.add(new_wishlist_item)
    db.commit()
    db.refresh(new_wishlist_item)
    return new_wishlist_item

def get_wishlist_items(db: Session, wishlist_id: int) -> list[WishlistItem]:
    return db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist_id).all()

def remove_from_wishlist(db: Session, product_id: int, wishlist_item_id: int) -> WishlistItem:
    existing_wishlist_item = db.query(WishlistItem).filter(
        WishlistItem.id == wishlist_item_id,
        WishlistItem.product_id
    ).first()
    if not existing_wishlist_item:
        raise HTTPException(status_code = 404, detail = "Item not found in Wishlist")
    db.delete(existing_wishlist_item)
    db.commit()
    return existing_wishlist_item

def clear_wishlist(db: Session, wishlist_id: int):
    db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist_id).delete()
    db.commit()