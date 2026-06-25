from fastapi import APIRouter, Depends
from typing import Annotated
from app.core.security import get_current_user
from app.core.database import get_session
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.order import OrderResponse
from app.services.order_service import checkout, get_order, user_orders
from app.services.cart_service import get_or_create_cart


router = APIRouter(
    prefix = "/orders",
    tags = ["orders"]
)

@router.post("/checkout")
def check_out(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)]):
    cart = get_or_create_cart(db, current_user.id)
    checkout(db, current_user.id, cart.id)
    return({"Message": "Order Successfully Placed"})

@router.get("/", response_model = list[OrderResponse])
def user_orders_get(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)]):
    return user_orders(db, current_user.id)

@router.get("/{order_id}", response_model = OrderResponse)
def order_get(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], order_id: int):
    return get_order(db, current_user.id, order_id)