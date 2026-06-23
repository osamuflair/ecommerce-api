from fastapi import FastAPI

app = FastAPI()

from app.api.v1.routes.users import router as users_router
from app.api.v1.routes.address import router as address_router
from app.api.v1.routes.cart import router as cart_router


app.include_router(users_router, prefix="/api/v1")
app.include_router(address_router, prefix="/api/v1")
app.include_router(cart_router, prefix="/api/v1")