"""Pydantic models for request/response validation.

This module defines Pydantic models used for validating request and response data
in the User Management API. It includes models for user creation, updates, and
data representation with proper validation rules.

Models:
    AddressBase: Base model for address validation
    UserBase: Base user model with common fields
    UserCreate: Model for user creation with password
    UserUpdate: Model for user updates with optional fields
    User: Complete user model for responses
"""

from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class AddressBase(BaseModel):
    """Base model for address validation.
    
    Attributes:
        street_address (str): Street address
        city (str): City name
        state (str): State/province
        country (str): Country name
        postal_code (str): Postal/ZIP code
    """
    street_address: str
    city: str
    state: str
    country: str
    postal_code: str

class UserBase(BaseModel):
    """Base user model with common fields.
    
    This model serves as the base for other user-related models,
    containing fields that are common across different operations.
    
    Attributes:
        email (EmailStr): Validated email address
        username (str): Username
        street_address (str): Street address
        city (str): City name
        state (str): State/province
        country (str): Country name
        postal_code (str): Postal/ZIP code
    """
    email: EmailStr
    username: str
    street_address: str
    city: str
    state: str
    country: str
    postal_code: str

class UserCreate(UserBase):
    """Model for user creation requests.
    
    Extends UserBase to include password field with validation.
    
    Attributes:
        password (str): Password with minimum length validation
    
    Note:
        Password must be at least 8 characters long
    """
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    """Model for user update requests.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        email (EmailStr, optional): New email address
        username (str, optional): New username
        password (str, optional): New password (min length: 8)
        street_address (str, optional): New street address
        city (str, optional): New city
        state (str, optional): New state/province
        country (str, optional): New country
        postal_code (str, optional): New postal code
        is_active (bool, optional): New account status
    """
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
    """Complete user model for responses.
    
    Extends UserBase to include system-managed fields.
    Used for sending user data in API responses.
    
    Attributes:
        id (int): User ID
        is_active (bool): Account status
        created_at (datetime): Account creation timestamp
        updated_at (datetime, optional): Last update timestamp
    
    Config:
        from_attributes: Enables ORM model mapping
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 