from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.services.cart_service import get_cart_items, clear_cart
from app.services.address_service import get_user_addresses
from fastapi import HTTPException

def checkout(db: Session, user_id: int, cart_id: int) -> Order:
    """
    Processes an order.
    
    Validates that the cart has items.
    Validates that the user has an address set, and if the user has a default delivery address.
    Adds user_id, address_id and a price of zero to a new order.
    Loops through the items in the cart:
        - Validates that the cart_item quantity is less than the available stock quantity.
        - Creates a new_order_item:
            - With order_id of the new created order.
            - Product_id and quantity correlating with the cart_item.
            - And the price corresponding with the current price of te product.
        - Decrease the quantity in stock with the quantity of the cart item.
        - Increment the order price with the price of the cart item.

    Args:
        db: DB session.
        user_id: ID of the user.
        cart_id: ID of the cart.

    Returns:
        The created Order model.

    Raises:
        HTTPException 404: If the cart has no item, and if there is no delivery address.
        HTTPException 409: If no default delivery is set, and if stock quantity is less than what is ordered.
    """
    existing_cart_items = get_cart_items(db, cart_id)
    if not existing_cart_items:
        raise HTTPException(status_code = 404, detail = "Cart is empty")    
    user_addresses = get_user_addresses(db, user_id)
    if not user_addresses:
        raise HTTPException(status_code = 404, detail = "Delivery address is not set")
    address_id = None
    for address in user_addresses:
        if address.is_default is True:
            address_id = address.id
            break
    if address_id is None:
        raise HTTPException(status_code = 409, detail = "Set default delivery address before proceeding")
    new_order = Order(
        user_id = user_id,
        total_price = 0,
        address_id = address_id,
    )
    db.add(new_order)
    db.flush()


    total_price: float = 0.00  
    for cart_item in existing_cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if cart_item.quantity > product.stock_quantity:
            raise HTTPException(status_code = 409, detail = f"Only {product.stock_quantity} units remaining in stock")
        new_order_item = OrderItem(
            order_id = new_order.id,
            product_id =cart_item.product_id,
            quantity = cart_item.quantity,
            price = cart_item.product.price
        )
        product.stock_quantity -= cart_item.quantity
        total_price += cart_item.quantity * cart_item.product.price
        db.add(new_order_item)

    new_order.total_price = total_price 
    clear_cart(db, cart_id)
    db.commit()
    db.refresh(new_order)
    return new_order

def update_order_status(db: Session, order_id: int, new_status: OrderStatus) -> Order:
    """
    Updates the status of an order.
    
    Checks if the order exists.
    Updates the order status.
    
    Args:
        db: DB session.
        order_id: ID of the order.
        new_status: The new status to set on the order (OrderStatus enum).
        
    Returns:
        The updated Order model.
        
    Raises:
        HTTPException 404: If order is not found.
    """
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code = 404, detail = "Order not found")
    existing_order.status = new_status
    db.commit()
    db.refresh(existing_order)
    return existing_order

def user_orders(db: Session, user_id: int) -> list[Order]:
    """Gets all user orders."""
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_order(db: Session, user_id: int, order_id: int) -> Order:
    """Gets a specific order belonging to the current user."""
    existing_order = db.query(Order).filter(Order.user_id == user_id, Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code = 404, detail = "Order not found")
    return existing_order

def get_all_orders(db: Session, status: OrderStatus | None = None, skip: int = 0, limit: int = 10) -> list[Order]:
    """Gets all orders. Optionally filters by status if provided."""
    if status is None:
        return db.query(Order).offset(skip).limit(limit).all()
    return db.query(Order).filter(Order.status == status).offset(skip).limit(limit).all()

def cancel_order(db: Session, user_id: int, order_id: int) -> Order:
    """
    Cancels a specific order.
    
    Validates that order exists.
    Validates that status is pending.
    Cancels the order and restores stock quantities for each item..
    
    Args:
        db: DB session.
        user_id: ID of user.
        order_id: ID of order.
        
    Returns:
        The cancelled Order model.

    Raises:
        HTTPException 404: If order does not exists.
        HTTPException 403: If the order cannot be cancelled.
        """
    existing_order = db.query(Order).filter(Order.user_id == user_id, Order.id == order_id).first()
    if not existing_order:
        raise HTTPException(status_code = 404, detail = "Order not found")
    if existing_order.status != OrderStatus.PENDING:
        raise HTTPException(status_code = 403, detail = "Order cannot be cancelled")
    for items in existing_order.order_items:
        product = db.query(Product).filter(Product.id == items.product_id).first()
        product.stock_quantity += items.quantity
    existing_order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(existing_order)
    return existing_order