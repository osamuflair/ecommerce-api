from pydantic import BaseModel, field_validator, ConfigDict

class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes = True)

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None