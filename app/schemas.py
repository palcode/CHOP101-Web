from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class AddressBase(BaseModel):
    street_address: str
    city: str
    state: str
    country: str
    postal_code: str

class UserBase(BaseModel):
    email: EmailStr
    username: str
    street_address: str
    city: str
    state: str
    country: str
    postal_code: str

class UserCreate(UserBase):
    password: constr(min_length=8)  # Add minimum password length validation

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[constr(min_length=8)] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 