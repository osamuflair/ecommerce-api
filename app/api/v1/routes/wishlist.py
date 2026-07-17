from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.services.wishlist_service import get_or_create_wishlist, add_to_wishlist, get_wishlist_items, remove_from_wishlist, clear_wishlist
from app.schemas.wishlist import WishlistItemResponse

router = APIRouter(
    prefix = "/wishlist",
    tags=["wishlist"]
)

@router.post("/items/{product_id}")
def wishlist_add(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], product_id: int):
    """Adds an item to the current users wishlist."""
    wishlist = get_or_create_wishlist(db, current_user.id)
    add_to_wishlist(db, wishlist.id, product_id)
    return ({"Message": "Sucessfully Added Item to Wishlist"})

@router.get("/", response_model = list[WishlistItemResponse])
def wishlist_item_get(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)]):
    """Gets the current user wishlist."""
    wishlist = get_or_create_wishlist(db, current_user.id)
    return get_wishlist_items(db, wishlist.id)

@router.delete("/items/{wishlist_item_id}")
def wishlist_item_remove(db: Annotated[Session, Depends(get_session)],  current_user: Annotated[User, Depends(get_current_user)], wishlist_item_id: int):
    """Deletes items from the current users wishlist."""
    wishlist = get_or_create_wishlist(db, current_user.id)
    remove_from_wishlist(db, wishlist.id, wishlist_item_id)
    return ({"Message": "Sucessfully Removed Item from Wishlist"})

@router.delete("/")
def wishlist_clear(db: Annotated[Session, Depends(get_session)],  current_user: Annotated[User, Depends(get_current_user)]):
    """Clears the current users wishlist."""
    wishlist = get_or_create_wishlist(db, current_user.id)
    clear_wishlist(db, wishlist.id)
    return ({"Message": "Sucessfully Cleared Wishlist"})