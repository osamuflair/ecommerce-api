from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate, CategoryUpdate
from fastapi import HTTPException

def create_category(db: Session, created_category: CategoryCreate) -> Category:
    """
    Creates a category for products.

    Validates that the category does not already exists.
    Creates category.

    Args:
        db: DB session.
        created_category: A CategoryCreate model that contains the name and description of the category.

    Returns:
        The created Category model.

    Raises:
        HTTPException 400: If the category already exists.
    """
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
    return new_category

def update_category(db: Session, category_id: int, updated_category: CategoryUpdate) -> Category:
    """
    Updates the name or/and description of a category.
    
    Validates that the category exists.
    Updates the category.

    Args:
        db: DB session.
        category_id: ID of the category
        updated_category: A CategoryUpdate model that contains the name or/and description of the category.

    Returns:
        The updated Category model.

    Raises:
        HTTPException 404: If the category does not exists.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found")
    if updated_category.name:
        category.name = updated_category.name
    if updated_category.description:
        category.description = updated_category.description
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int) -> Category:
    """
    Deletes a category.
    
    Validates that the category exists.
    Validates that the category has no existing products.
    Deletes the category.

    Args:
        db: DB session.
        category_id: ID of the category.

    Returns:
        The deleted Category model.

    Raises:
        HTTPException 404: If the category does not exists.
        HTTPException 409: If the category has existing products.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code = 404, detail = "Category not found")
    existing_products = db.query(Product).filter(Product.category_id == category_id).first()
    if existing_products:
        raise HTTPException(status_code=409, detail="Category has existing products and cannot be deleted")
    db.delete(category)
    db.commit()
    return category

def get_category_by_id(db: Session, category_id: int) -> Category:
    """
    Gets a category by its ID.
    
    Validates that the category exists.

    Args:
        db: DB session.
        category_id: ID of the category

    Returns:
        The Category model.

    Raises:
        HTTPException 404: If the category does not exists.
    """
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if not existing_category:
        raise HTTPException(status_code = 404, detail = "category not found")
    return existing_category

def get_all_category(db: Session) -> list[Category]:
    """Gets all the categories"""
    return db.query(Category).all()