from pydantic import BaseModel, ConfigDict
from datetime import datetime

class OrderItemCreate(BaseModel):
    quantity:int

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes = True)

class OrderItemsUpdate(BaseModel):
    quantity: int

class OrderResponse(BaseModel):
    id: int
    order_items: list["OrderItemResponse"]
    total_price: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)