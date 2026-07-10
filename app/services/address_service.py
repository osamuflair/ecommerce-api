from sqlalchemy.orm import Session
from app.models.address import Address
from app.models.order import Order
from app.schemas.address import AddressCreate,  AddressUpdate
from fastapi import HTTPException

def create_address(db: Session, user_id: int, created_address: AddressCreate) -> Address:
    """Creates a new address for the current user."""
    new_address = Address(
        user_id = user_id,
        full_name = created_address.full_name,
        phone_number = created_address.phone_number,
        street_address = created_address.street_address,
        city = created_address.city,
        state = created_address.state
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

def update_address(db: Session, user_id: int, address_id: int, updated_address: AddressUpdate) -> Address:
    """
    Updates the current user address(phone_number, street_address, city, or/and state).
    
    Validates that the address exists, and that it belongs to the user.
    Updates the user address.

    Args:
        db: DB session.
        user_id: ID of the user.
        address_id: ID of the address.
        updated_address: an AddressUpdate model that contains what the user wants to change.

    Returns:
        The updated address model.

    Raises:
        HttpException 404: If the user does not exists, or if the address does not belong to the user.
    """
    existing_address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()
    if not existing_address:
        raise HTTPException(status_code = 404, detail = "Address not found")
    if updated_address.phone_number:
        existing_address.phone_number = updated_address.phone_number
    if updated_address.street_address:
        existing_address.street_address = updated_address.street_address
    if updated_address.city:
        existing_address.city = updated_address.city
    if updated_address.state:
        existing_address.state = updated_address.state
    db.commit()
    db.refresh(existing_address)
    return existing_address

def set_default_address(db: Session, user_id: int, address_id: int) -> Address:
    """
    Sets a default address for a user, by changing is_default to True.
    
    Validates that the address exists, and that it belongs to the user.
    Checks if current user has any address set as default and removes it.
    set address as default.
    
    Args:
        db: DB session.
        user_id: ID of user.
        address_id: Address that wants to be set to default.
        
    Returns:
        The new default address model.
        
    Raises:
        HTTPException 404: If the user does not exists, or if the address does not belong to the user.
        """
    existing_address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()
    if not existing_address:
        raise HTTPException(status_code = 404, detail = "Address not found")
    db.query(Address).filter(Address.user_id == existing_address.user_id).update({"is_default": False})
    existing_address.is_default = True
    db.commit()
    db.refresh(existing_address)
    return existing_address

def delete_address(db: Session, user_id: int, address_id: int) -> Address:
    """
    Deletes a user address.
    
    Validates that the address exists, and that it belongs to the user.
    Validates that the address has not been used for any order.
    Deletes address.

    Args:
        db: DB session.
        user_id: ID of user.
        address_id: ID of the address to delete.

    Returns:
        Returns the deleted address model

    Raises:
        HTTPException 404: If the user does not exists, or if the address does not belongs to the user.
        HTTPException 409: If the address is attached to an existing order.
        """
    existing_address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()
    if not existing_address:
        raise HTTPException(status_code = 404, detail = "Address not found")
    existing_orders = db.query(Order).filter(Order.address_id == address_id).first()
    if existing_orders:
        raise HTTPException(status_code=409, detail="Address is attached to an existing order and cannot be deleted")
    db.delete(existing_address)
    db.commit()
    return existing_address

def get_user_addresses(db: Session, user_id: int) -> list[Address]:
    """Gets all the addresses of the current user."""
    return db.query(Address).filter(Address.user_id == user_id).all()