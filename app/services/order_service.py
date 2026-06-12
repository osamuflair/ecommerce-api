from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import OrderItemCreate, OrderItemsUpdate
from app.services.cart_service import get_cart_items, clear_cart
from app.services.address_service import get_user_addresses
from fastapi import HTTPException

def checkout(db: Session, user_id: int, cart_id: int) -> Order:
    existing_cart_items = get_cart_items(db, cart_id)
    if not existing_cart_items:
        raise HTTPException(status_code = 404, detail = "Cart is empty")    
    user_addresses = get_user_addresses(db, user_id)
    if not user_addresses:
        raise HTTPException(status_code = 404, detail = "Delivery address is not set")
    for address in user_addresses:
        if address.is_default is True:
            address_id = address.id
            break
        address_id = address.id
    new_order = Order(
        user_id = user_id,
        total_price = 0,
        address_id = address_id,
    )
    db.add(new_order)
    db.flush()

    total_price: float = 0.00  
    for cart_item in existing_cart_items:
        new_order_item = OrderItem(
            order_id = new_order.id,
            product_id =cart_item.product_id,
            quantity = cart_item.quantity,
            price = cart_item.product.price
        )
        total_price += cart_item.quantity * cart_item.product.price
        db.add(new_order_item)

    new_order.total_price = total_price 
    clear_cart(db, cart_id)
    db.commit()
    db.refresh(new_order)
    return new_order