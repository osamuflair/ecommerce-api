from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: int | None = None