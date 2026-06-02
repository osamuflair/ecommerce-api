from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(unique = True)
    description: Mapped[str]
    products: Mapped[list["Product"]] = relationship(back_populates = "category", lazy = "select")