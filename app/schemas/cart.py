from pydantic import BaseModel, ConfigDict

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes = True)

class CartItemUpdate(BaseModel):
    quantity: int

class CartResponse(BaseModel):
    id: int
    user_id: int
    cart_items: list["CartItemResponse"]

    model_config = ConfigDict(from_attributes = True)
