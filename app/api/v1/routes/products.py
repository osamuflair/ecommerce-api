from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import require_admin
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import create_product, update_product, delete_product, get_all_product, get_product_by_id

router = APIRouter(
    prefix = "/products",
    tags = ["products"]
)

@router.post("/")
def product_create(db: Annotated[Session, Depends(get_session)], admin: Annotated[User, Depends(require_admin)], created_product: ProductCreate):
    create_product(db, created_product)
    return ({"message": "Product Successfully Created"})

@router.put("/{product_id}")
def product_update(db: Annotated[Session, Depends(get_session)], admin: Annotated[User, Depends(require_admin)], updated_product: ProductUpdate, product_id: int):
    update_product(db, product_id, updated_product)
    return ({"message": "Product Successfully updated"})

@router.delete("/{product_id}")
def product_delete(db: Annotated[Session, Depends(get_session)], admin: Annotated[User, Depends(require_admin)], product_id: int):
    delete_product(db, product_id)
    return ({"message": "Product Successfully Deleted"})

@router.get("/", response_model = list[ProductResponse])
def product_get_all(db: Annotated[Session, Depends(get_session)]):
    return get_all_product(db)

@router.get("/{product_id}", response_model = ProductResponse)
def product_get_by_id(db: Annotated[Session, Depends(get_session)], product_id: int):
    return get_product_by_id(db, product_id)