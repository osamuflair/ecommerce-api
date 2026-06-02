from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey, func

from app.core.database import Base


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str]
    price: Mapped[float]
    stock_quantity: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())
    category: Mapped["Category"] = relationship(back_populates = "products", lazy = "select")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates = "product", lazy = "select")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates = "product", lazy = "select")
    wishlist_item: Mapped["WishlistItem"] = relationship(back_populates = "product", lazy = "select")