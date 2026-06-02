from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.core.database import Base

class Wishlist(Base):
    __tablename__ = "wishlist"
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique = True)
    user: Mapped["User"] = relationship(back_populates = "wishlist", lazy = "select")
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(back_populates = "wishlist", lazy = "select")

class WishlistItem(Base):
    __tablename__ = "wishlist_item"
    id: Mapped[int] = mapped_column(primary_key = True)
    wishlist_id: Mapped[int] = mapped_column(ForeignKey("wishlist.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    wishlist: Mapped["Wishlist"] = relationship(back_populates = "wishlist_items", lazy = "select")
    product: Mapped["Product"] = relationship(back_populates = "wishlist_item", lazy = "select")