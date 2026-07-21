from pydantic import BaseModel, field_validator, ConfigDict, Field

import re

PHONE_PATTERN = re.compile(r"^(\+234|0)[789][01]\d{8}$")

from enum import Enum

class NigeriaState(str, Enum):
    ABIA = "Abia"
    ADAMAWA = "Adamawa"
    AKWA_IBOM = "Akwa Ibom"
    ANAMBRA = "Anambra"
    BAUCHI = "Bauchi"
    BAYELSA = "Bayelsa"
    BENUE = "Benue"
    BORNO = "Borno"
    CROSS_RIVER = "Cross River"
    DELTA = "Delta"
    EBONYI = "Ebonyi"
    EDO = "Edo"
    EKITI = "Ekiti"
    ENUGU = "Enugu"
    FCT = "FCT"
    GOMBE = "Gombe"
    IMO = "Imo"
    JIGAWA = "Jigawa"
    KADUNA = "Kaduna"
    KANO = "Kano"
    KATSINA = "Katsina"
    KEBBI = "Kebbi"
    KOGI = "Kogi"
    KWARA = "Kwara"
    LAGOS = "Lagos"
    NASARAWA = "Nasarawa"
    NIGER = "Niger"
    OGUN = "Ogun"
    ONDO = "Ondo"
    OSUN = "Osun"
    OYO = "Oyo"
    PLATEAU = "Plateau"
    RIVERS = "Rivers"
    SOKOTO = "Sokoto"
    TARABA = "Taraba"
    YOBE = "Yobe"
    ZAMFARA = "Zamfara"

class AddressCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=50)
    phone_number: str
    street_address: str
    city: str
    state: NigeriaState

    @field_validator("phone_number")
    @classmethod
    def valid_phone(cls, v):
        if not PHONE_PATTERN.match(v):
            raise ValueError("invalid phone number")
        return v
        
        
class AddressResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone_number: str
    street_address: str
    city: str
    state: str
    is_default: bool
    
    model_config = ConfigDict(from_attributes=True)


class AddressUpdate(BaseModel):
    phone_number: str | None = None
    street_address: str | None = None
    city: str | None = None
    state: NigeriaState | None = None

    @field_validator("phone_number")
    @classmethod
    def valid_phone(cls, v):
        if v is None:
            return v
        if not PHONE_PATTERN.match(v):
            raise ValueError("invalid phone number")
        return v