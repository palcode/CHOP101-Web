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

from pydantic import (
    BaseModel,
    EmailStr,
    constr,
    validator,
    Field
)
from typing import Optional
from datetime import datetime
import re

# Constants for validation
MAX_LENGTH = 100
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 72  # bcrypt maximum
POSTAL_CODE_PATTERN = r'^\d{5}(-\d{4})?$'  # US format, adjust as needed
USERNAME_PATTERN = r'^[a-zA-Z0-9_-]{3,32}$'

class AddressBase(BaseModel):
    """Base model for address validation.
    
    Attributes:
        street_address (str): Street address
        city (str): City name
        state (str): State/province
        country (str): Country name
        postal_code (str): Postal/ZIP code
    """
    street_address: constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)
    city: constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)
    state: constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)
    country: constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)
    postal_code: constr(strip_whitespace=True)

    @validator('postal_code')
    def validate_postal_code(cls, v):
        """Validate postal code format."""
        if not re.match(POSTAL_CODE_PATTERN, v):
            raise ValueError('Invalid postal code format')
        return v

    @validator('*')
    def no_html_in_strings(cls, v):
        """Prevent HTML injection in string fields."""
        if isinstance(v, str):
            if '<' in v or '>' in v:
                raise ValueError('HTML tags are not allowed')
        return v

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
    email: EmailStr = Field(..., description="Valid email address")
    username: constr(regex=USERNAME_PATTERN) = Field(
        ...,
        description="Username (3-32 chars, alphanumeric, underscore, hyphen)"
    )
    street_address: str
    city: str
    state: str
    country: str
    postal_code: str

class UserCreate(UserBase):
    """Model for user creation requests.
    
    Extends UserBase to include password field with validation.
    
    Attributes:
        password (str): Password with security requirements
    
    Note:
        Password must meet the following criteria:
        - 8-72 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        - Contains at least one special character
    """
    password: constr(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)

    @validator('password')
    def validate_password(cls, v):
        """Validate password complexity."""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdate(BaseModel):
    """Model for user update requests.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        email (EmailStr, optional): New email address
        username (str, optional): New username
        password (str, optional): New password with security requirements
        street_address (str, optional): New street address
        city (str, optional): New city
        state (str, optional): New state/province
        country (str, optional): New country
        postal_code (str, optional): New postal code
        is_active (bool, optional): New account status
    """
    email: Optional[EmailStr] = None
    username: Optional[constr(regex=USERNAME_PATTERN)] = None
    password: Optional[constr(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH)] = None
    street_address: Optional[constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)] = None
    city: Optional[constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)] = None
    state: Optional[constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)] = None
    country: Optional[constr(min_length=1, max_length=MAX_LENGTH, strip_whitespace=True)] = None
    postal_code: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('password')
    def validate_password(cls, v):
        """Validate password complexity if provided."""
        if v is not None:
            if not re.search(r'[A-Z]', v):
                raise ValueError('Password must contain at least one uppercase letter')
            if not re.search(r'[a-z]', v):
                raise ValueError('Password must contain at least one lowercase letter')
            if not re.search(r'\d', v):
                raise ValueError('Password must contain at least one number')
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
                raise ValueError('Password must contain at least one special character')
        return v

    @validator('postal_code')
    def validate_postal_code(cls, v):
        """Validate postal code format if provided."""
        if v is not None and not re.match(POSTAL_CODE_PATTERN, v):
            raise ValueError('Invalid postal code format')
        return v

    @validator('*')
    def no_html_in_strings(cls, v):
        """Prevent HTML injection in string fields."""
        if isinstance(v, str):
            if '<' in v or '>' in v:
                raise ValueError('HTML tags are not allowed')
        return v

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