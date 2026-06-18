from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.user import User
from app.core.database import get_session
from app.schemas.user import UserResponse
from app.core.security import get_current_user
from app.services.user_service import create_user, update_user, deactivate_user
from app.services.auth_service import log_in
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter(
    prefix = "/users",
    tags = ["user"]
)

@router.post("/register")
def user_registration(user_details: UserCreate, db: Annotated[Session, Depends(get_session)]):
        create_user(db, user_details)
        return({"Message": "Successfully Registered"})

@router.post("/login")
def user_log_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_session)]):
    token = log_in(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model = UserResponse)
def get_user(current_user: Annotated[User, Depends(get_current_user)]):
      return current_user

@router.put("/me")
def user_update(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_session)], updated_data: UserUpdate):
    update_user(db, current_user.id, updated_data)
    return({"Message": "Details Successfully Updated"})

@router.delete("/me")
def user_deactivate(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_session)]):
    deactivate_user(db, current_user.id)
    return({"Message": "Account Successfully Deleted"})