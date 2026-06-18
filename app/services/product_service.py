from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from fastapi import HTTPException

def create_product(db: Session, created_product: ProductCreate) -> ProductResponse:
    existing_product = db.query(Product).filter(Product.name == created_product.name).first()
    if existing_product:
        raise HTTPException(status_code = 400, detail = "Product already exists")
    new_product = Product(
        name = created_product.name,
        description = created_product.description,
        price = created_product.price,
        stock_quantity = created_product.stock_quantity,
        category_id = created_product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return ProductResponse(new_product)

def update_product(db: Session, product_id: int, updated_product: ProductUpdate) -> ProductResponse:
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    if updated_product.name:
        existing_product.name = updated_product.name
    if updated_product.description:
        existing_product.description = updated_product.description
    if updated_product.price:
        existing_product.price = updated_product.price
    if updated_product.category_id:
        existing_product.category_id = updated_product.category_id
    db.commit()
    db.refresh(existing_product)
    return ProductResponse(existing_product)

def delete_product(db: Session, product_id: int) -> ProductResponse:
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    db.delete(existing_product)
    db.commit()
    return ProductResponse(existing_product)

def get_product_by_id(db: Session, product_id: int) -> ProductResponse | None:
    return ProductResponse(db.query(Product).filter(Product.id == product_id).first())

def get_all_product(db: Session) -> list[ProductResponse]:
    return ProductResponse(db.query(Product).all())