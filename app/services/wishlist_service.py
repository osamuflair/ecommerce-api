from sqlalchemy.orm import Session
from app.models.wishlist import WishlistItem, Wishlist
from fastapi import HTTPException

def add_to_wishlist(db: Session, wishlist_id: int, product_id: int) -> WishlistItem:
    """
    Adds an item to a user wishlist
    
    Validates that the item is not already in the wishlist.
    
    Args:
        db: DB session.
        wishlist_id: ID of wishlist.
        product_id: ID of product.
        
    Returns:
        The new WishlistItem model.
        
    Raises:
        HTTPException 400: If item is already in the wishlist."""
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
    """Gets all wishlist items"""
    return db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist_id).all()

def remove_from_wishlist(db: Session, wishlist_id: int, wishlist_item_id: int) -> WishlistItem:
    """
    Removes an item from wishlist.
    
    Validates that the wishlistitem exists.
    Deletes wishlistitem.
    
    Args:
        db: DB session.
        wishlist_id: ID of the wishlist.
        wishlist_item_id: ID of the wishlist_item.

    Returns:
        The WishlistItem model.

    Raises:
        HTTPException 404: If item is not in the wishlist. 
    """
    existing_wishlist_item = db.query(WishlistItem).filter(
        WishlistItem.id == wishlist_item_id,
        WishlistItem.wishlist_id == wishlist_id
    ).first()
    if not existing_wishlist_item:
        raise HTTPException(status_code = 404, detail = "Item not found in Wishlist")
    db.delete(existing_wishlist_item)
    db.commit()
    return existing_wishlist_item

def clear_wishlist(db: Session, wishlist_id: int):
    """Clears all items in the wishlist"""
    db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist_id).delete()
    db.commit()

def get_or_create_wishlist(db: Session, user_id: int) -> Wishlist:
    """
    Gets a users wishlist if it exists, or creates the wishlist first if it does not exists.
    """
    wishlist = db.query(Wishlist).filter(Wishlist.user_id == user_id).first()
    if not wishlist:
        new_wishlist = Wishlist(user_id = user_id)
        db.add(new_wishlist)
        db.commit()
        db.refresh(new_wishlist)
        return new_wishlist
    return wishlist