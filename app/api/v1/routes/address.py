from fastapi import APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate
from app.services.address_service import create_address, get_user_addresses, update_address, set_default_address, delete_address

router = APIRouter(
    prefix = "/addresses",
    tags = ["address"]
)

@router.post("/")
def address_creation(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_session)], created_address: AddressCreate):
    """Creates a new delivery address for the current user."""
    create_address(db, current_user.id, created_address)
    return({"Message": "Address Successfully Created"})

@router.get("/", response_model = list[AddressResponse])
def get_addresses(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_session)]):
    """Gets all the current user addresses."""
    return get_user_addresses(db, current_user.id)

@router.put("/{address_id}")
def address_update(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_session)], updated_address: AddressUpdate, address_id: int):
    """Updates a current user address."""
    update_address(db, current_user.id, address_id, updated_address)
    return({"Message": "Address Successfully Updated"})

@router.put("/{address_id}/default")
def default_address(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_session)], address_id: int):
    """Sets a specific address of the current user to default."""
    set_default_address(db, current_user.id, address_id)
    return({"Message": "Default Address Successfully Set"})

@router.delete("/{address_id}")
def address_delete(current_user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_session)], address_id: int):
    """Deletes a specific address of the current user."""
    delete_address(db, current_user.id, address_id)
    return({"Message": "Address Successfully Deleted"})