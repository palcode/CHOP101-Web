from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None

class UserCreate(UserBase):
    id: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None
    is_active: Optional[bool] = None

class UserProfileBase(BaseModel):
    address: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    user_id: str

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile: Optional[UserProfile] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: str

class GoogleAuthRequest(BaseModel):
    credential: str

class Session(BaseModel):
    id: str
    user_id: str
    token: str
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 