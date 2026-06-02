from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from datetime import datetime

from app.core.database import Base

class Cart(Base):
    __tablename__ = "cart"
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique = True)
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())
    user: Mapped["User"] = relationship(back_populates = "cart", lazy = "select")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates = "cart", lazy = "select")

class CartItem(Base):
    __tablename__ = "cart_item"
    id: Mapped[int] = mapped_column(primary_key = True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    quantity: Mapped[int]
    cart: Mapped["Cart"] = relationship(back_populates = "cart_items", lazy = "select")
    product: Mapped["Product"] = relationship(back_populates = "cart_items", lazy = "select")