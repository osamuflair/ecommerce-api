from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.address import AddressCreate,  AddressUpdate
from fastapi import HTTPException

def create_address(db: Session, user_id: int, created_address: AddressCreate) -> Address:
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

def update_address(db: Session, address_id: int, updated_address: AddressUpdate) -> Address:
    existing_address = db.query(Address).filter(Address.id == address_id).first()
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

def set_default_address(db: Session, address_id: int) -> Address:
    existing_address = db.query(Address).filter(Address.id == address_id).first()
    if not existing_address:
        raise HTTPException(status_code = 404, detail = "Address not found")
    db.query(Address).filter(Address.user_id == existing_address.user_id).update({"is_default": False})
    existing_address.is_default = True
    db.commit()
    db.refresh(existing_address)
    return existing_address

def delete_address(db: Session, address_id: int) -> Address:
    existing_address = db.query(Address).filter(Address.id == address_id).first()
    if not existing_address:
        raise HTTPException(status_code = 404, detail = "Address not found")
    db.delete(existing_address)
    db.commit()
    return existing_address

def get_user_addresses(db: Session, user_id: int) -> list[Address]:
    return db.query(Address).filter(Address.user_id == user_id).all()