from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func, Enum as SQLEnum
from enum import Enum

from app.core.database import Base

class UserRole(Enum):
    CUSTOMER = "customer"
    STAFF = "staff"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(unique = True)
    email: Mapped[str] = mapped_column(unique = True)
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name = "user_role_enum"), nullable = False, default = UserRole.CUSTOMER)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())