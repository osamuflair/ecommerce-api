from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from fastapi import HTTPException

def create_category(db: Session, created_category: CategoryCreate) -> CategoryResponse:
    existing_category = db.query(Category).filter(Category.name == created_category.name).first()
    if existing_category:
        raise HTTPException(status_code = 400, detail = "Category already exists")
    new_category = Category(
        name = created_category.name,
        description = created_category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return CategoryResponse(new_category)

def update_category(db: Session, category_id: int, updated_category: CategoryUpdate) -> CategoryResponse:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found")
    if updated_category.name:
        category.name = updated_category.name
    if updated_category.description:
        category.description = updated_category.description
    db.commit()
    db.refresh(category)
    return CategoryResponse(category)

def delete_category(db: Session, category_id: int) -> CategoryResponse:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found")
    db.delete(category)
    db.commit()
    return CategoryResponse(category)

def get_category_by_id(db: Session, category_id: int) -> CategoryResponse | None:
    return CategoryResponse(db.query(Category).filter(Category.id == category_id).first())

def get_all_category(db: Session) -> list[CategoryResponse]:
    return CategoryResponse(db.query(Category).all())