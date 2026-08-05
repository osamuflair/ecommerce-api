from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
import re

UPPER = re.compile(r"[A-Z]")
LOWER = re.compile(r"[a-z]")
DIGIT = re.compile(r"\d")
SPECIAL = re.compile(r"[^A-Za-z0-9]")
ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")

RESERVED_USERNAME = {
    "admin", "root", "system", "null", "user"
}

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
        if len(v) >= 8:
            if UPPER.search(v) and LOWER.search(v) and DIGIT.search(v) and SPECIAL.search(v):
                return v
            raise ValueError("password must contain at least one uppercase and lowercase letter, a number and a special character")
        raise ValueError("password must 8 characters")
    
    @field_validator("username")
    @classmethod
    def valid_username(cls, v):
        if len(v) < 3:
            raise ValueError("username must have a minimum of 3 characters")
        if len(v) > 20:
            raise ValueError("username must have a maximum 20 characters")
        if v in RESERVED_USERNAME:
            raise ValueError("username is reserved")
        if v[0] == "_" or v[-1] == "_":
            raise ValueError("username cannot start or end with an underscore")
        if ALLOWED_PATTERN.search(v):
            return v
        raise ValueError("username must contain, letters, numbers and underscore")

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    
    @field_validator("username")
    @classmethod
    def valid_username(cls, v):
        if v is None:
            return v
        if len(v) < 3:
            raise ValueError("username must have a minimum of 3 characters")
        if len(v) > 20:
            raise ValueError("username must have a maximum 20 characters")
        if v in RESERVED_USERNAME:
            raise ValueError("username is reserved")
        if v[0] == "_" or v[-1] == "_":
            raise ValueError("username cannot start or end with an underscore")
        if ALLOWED_PATTERN.search(v):
            return v
        raise ValueError("username must contain, letters, numbers and underscore")

class RefreshTokenRequest(BaseModel):
    refresh_token: str