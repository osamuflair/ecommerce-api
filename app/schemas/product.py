from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(min_length= 2, max_length= 100) 
    description: str = Field(min_length=10, max_length=1000)
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
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
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=1000)
    price: float | None = Field(default=None, gt=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    category_id: int | None = None