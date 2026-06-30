from fastapi import FastAPI

app = FastAPI()

from app.api.v1.routes.users import router as users_router
from app.api.v1.routes.address import router as address_router
from app.api.v1.routes.cart import router as cart_router
from app.api.v1.routes.wishlist import router as wishlist_router
from app.api.v1.routes.orders import router as order_router
from app.api.v1.routes.categories import router as category_router
from app.api.v1.routes.products import router as product_router

app.include_router(users_router, prefix="/api/v1")
app.include_router(address_router, prefix="/api/v1")
app.include_router(cart_router, prefix="/api/v1")
app.include_router(wishlist_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")