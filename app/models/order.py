from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, Enum as SQLEnum
from enum import Enum
from datetime import datetime

from app.core.database import Base


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    total_price: Mapped[float]
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus, name = "order_status_enum"), nullable = False, default = OrderStatus.PENDING,  server_default = "PENDING")
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())
    user: Mapped["User"] = relationship(back_populates = "orders", lazy = "select")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates = "order", lazy = "select")

class OrderItem(Base):
    __tablename__ = "order_item"
    id: Mapped[int] = mapped_column(primary_key = True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int]
    price: Mapped[float]
    order: Mapped["Order"] = relationship(back_populates = "order_items", lazy = "select")
    product: Mapped["Product"] = relationship(back_populates = "order_items", lazy = "select")