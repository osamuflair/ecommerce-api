from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartItemResponse
from app.services.cart_service import get_or_create_cart, add_cart_item, update_cart_item, remove_cart_item, clear_cart, get_cart_items

router = APIRouter(
    prefix = "/cart",
    tags = ["cart"]
)

@router.post("/items/")
def cart_item_add(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], created_cart_item: CartItemCreate):
    """Adds an item to the current users cart."""
    cart = get_or_create_cart(db, current_user.id)
    add_cart_item(db, created_cart_item, cart.id)
    return({"Message": "Item Successfully Added to Cart"})

@router.put("/items/{cart_item_id}")
def cart_item_update(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], updated_cart_item: CartItemUpdate, cart_item_id: int):
    """Updates an item in the current users cart."""
    cart = get_or_create_cart(db, current_user.id)
    update_cart_item(db, cart.id, updated_cart_item, cart_item_id)
    return ({"Message": "Item Successfully Updated"})

@router.delete("/items/{cart_item_id}")
def cart_item_removal(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], cart_item_id: int):
    """Deletes an item from the current users cart."""
    cart = get_or_create_cart(db, current_user.id)
    remove_cart_item(db, cart.id, cart_item_id)
    return ({"Message": "Item Successfully Removed from Cart"})

@router.delete("/")
def cart_clear(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)]):
    """Clears the current users cart."""
    cart = get_or_create_cart(db, current_user.id)
    clear_cart(db, cart.id)
    return ({"Message": "Cart Successfully Cleared"})

@router.get("/", response_model = list[CartItemResponse])
def cart_items_get(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)]):
    """Gets the current users cart."""
    cart = get_or_create_cart(db, current_user.id)
    return get_cart_items(db, cart.id)
