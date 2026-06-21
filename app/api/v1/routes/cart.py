from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate
from app.services.cart_service import get_or_create_cart, add_cart_item

router = APIRouter(
    prefix = "/cart",
    tags = ["cart"]
)

@router.post("/items/")
def cart_item_add(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], created_cart_item: CartItemCreate):
    cart = get_or_create_cart(db, current_user.id)
    add_cart_item(db, created_cart_item, cart.id, created_cart_item.product_id)
    return({"Message": "Item Successfully Added to Cart"})
