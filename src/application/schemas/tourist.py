from pydantic import BaseModel, EmailStr, Field

class CreateTouristRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UpdatePreferencesRequest(BaseModel):
    travel_type: str
    nights: int = Field(..., ge=1)
    group_size: int = Field(..., ge=1)
