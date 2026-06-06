from pydantic import BaseModel, ConfigDict

class WishlistItemResponse(BaseModel):
    id: int
    wishlist_id: int
    product_id: int

    model_config = ConfigDict(from_attributes = True)

class WishlistResponse(BaseModel):
    id: int
    user_id: int
    wishlist_items: list[WishlistItemResponse]

    model_config = ConfigDict(from_attributes = True)