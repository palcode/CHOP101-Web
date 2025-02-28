"""SQLAlchemy models for the User Management API.

This module defines the database models using SQLAlchemy ORM.
It includes the User model with all necessary fields for user management and address information.

Models:
    User: Represents a user in the system with personal and address information
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """User model representing a user in the system.
    
    This model stores user information including authentication details,
    address information, and account status. It includes automatic timestamp
    management for created_at and updated_at fields.
    
    Attributes:
        id (int): Primary key
        email (str): User's email address (unique)
        username (str): User's username (unique)
        hashed_password (str): Bcrypt hashed password
        is_active (bool): Account status flag
        street_address (str): Street address
        city (str): City name
        state (str): State/province
        country (str): Country name
        postal_code (str): Postal/ZIP code
        created_at (datetime): Timestamp of user creation
        updated_at (datetime): Timestamp of last update
    
    Note:
        The email and username fields are indexed and unique to ensure
        fast lookups and prevent duplicates.
    """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # Address fields
    street_address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 