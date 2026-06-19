from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.core.database import Base

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    full_name: Mapped[str]
    phone_number: Mapped[str]
    street_address: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    is_default: Mapped[bool] = mapped_column(default = False)
    user: Mapped["User"] = relationship(back_populates = "addresses", lazy = "select")
    orders: Mapped[list["Order"]] = relationship(back_populates = "address", lazy = "select")