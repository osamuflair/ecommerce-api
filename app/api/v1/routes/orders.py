from fastapi import APIRouter, Depends
from typing import Annotated
from app.core.security import get_current_user, require_staff
from app.core.database import get_session
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.order import OrderResponse
from app.models.order import OrderStatus
from app.services.order_service import checkout, get_order, user_orders, get_all_orders, update_order_status, cancel_order
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

@router.get("/all", response_model = list[OrderResponse])
def orders_get_all(db: Annotated[Session, Depends(get_session)], staff: Annotated[User, Depends(require_staff)], status: OrderStatus | None = None):
    return get_all_orders(db, status)

@router.get("/{order_id}", response_model = OrderResponse)
def order_get(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], order_id: int):
    return get_order(db, current_user.id, order_id)

@router.put("/{order_id}/status")
def order_status_update(db: Annotated[Session, Depends(get_session)], staff: Annotated[User, Depends(require_staff)], new_status: OrderStatus, order_id: int):
    update_order_status(db, order_id, new_status)
    return({"Message": "Order Status Successfully Updated"})

@router.put("/{order_id}/cancel")
def order_cancellation(db: Annotated[Session, Depends(get_session)], current_user: Annotated[User, Depends(get_current_user)], order_id: int):
    cancel_order(db, current_user.id, order_id)
    return({"Message": "Order Successfully Cancelled"})