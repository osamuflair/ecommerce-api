from fastapi import APIRouter, Depends
from app.services.category_service import create_category, update_category, delete_category, get_all_category, get_category_by_id
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import get_current_user, require_admin
from app.models.user import User

router = APIRouter(
    prefix = "/categories",
    tags = ["categories"]
)

@router.post("/")
def category_create(db: Annotated[Session, Depends(get_session)], admin: Annotated[User, Depends(require_admin)], created_category: CategoryCreate):
    """Creates a new category for products."""
    create_category(db, created_category)
    return {"Message": "Category Successfully Created"}

@router.put("/{category_id}")
def category_update(db: Annotated[Session, Depends(get_session)], admin: Annotated[User, Depends(require_admin)], category_id: int, updated_category: CategoryUpdate):
    """Updates an existing category."""
    update_category(db, category_id, updated_category)
    return {"Message": "Category Successfully Updated"}

@router.delete("/{category_id}")
def category_delete(db: Annotated[Session, Depends(get_session)], admin: Annotated[User, Depends(require_admin)], category_id: int):
    """Deletes a category."""
    delete_category(db, category_id)
    return {"Message": "Category Successfully Deleted"}

@router.get("/", response_model = list[CategoryResponse])
def categories_get_all(db: Annotated[Session, Depends(get_session)]):
    """Gets all categories."""
    return get_all_category(db)

@router.get("/{category_id}", response_model = CategoryResponse)
def category_get_by_id(db: Annotated[Session, Depends(get_session)], category_id: int):
    """Gets a specific category."""
    return get_category_by_id(db, category_id)