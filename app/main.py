"""FastAPI User Management API with CRUD operations.

This module implements a RESTful API for user management with the following features:
- User creation with password hashing
- User retrieval with filtering options
- User updates with partial update support
- User deletion
- Address management
- Input validation using Pydantic
- SQLite database with SQLAlchemy ORM

The API includes proper error handling, validation, and follows REST best practices.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, database
from typing import List, Optional
from passlib.context import CryptContext

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="User Management API",
    description="API for managing users with address information"
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CRUD Operations
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Create a new user.
    
    Creates a new user with the provided information, including address details.
    Performs validation for unique email and username, and hashes the password.
    
    Args:
        user (UserCreate): User data including email, username, password, and address
        db (Session): Database session dependency
    
    Returns:
        User: Created user information
    
    Raises:
        HTTPException: If email or username already exists
    """
    # Check if email exists
    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        street_address=user.street_address,
        city=user.city,
        state=user.state,
        country=user.country,
        postal_code=user.postal_code
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    """Retrieve users with optional filtering.
    
    Gets a list of users with pagination support and optional location-based filtering.
    
    Args:
        skip (int): Number of records to skip (default: 0)
        limit (int): Maximum number of records to return (default: 100)
        city (str, optional): Filter by city
        state (str, optional): Filter by state
        country (str, optional): Filter by country
        db (Session): Database session dependency
    
    Returns:
        List[User]: List of users matching the criteria
    """
    query = db.query(models.User)
    
    # Apply filters if provided
    if city:
        query = query.filter(models.User.city == city)
    if state:
        query = query.filter(models.User.state == state)
    if country:
        query = query.filter(models.User.country == country)
    
    users = query.offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    """Retrieve a specific user by ID.
    
    Args:
        user_id (int): ID of the user to retrieve
        db (Session): Database session dependency
    
    Returns:
        User: User information
    
    Raises:
        HTTPException: If user is not found
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(database.get_db)
):
    """Update a user's information.
    
    Supports partial updates of user information. Only provided fields will be updated.
    Validates email and username uniqueness if they are being updated.
    
    Args:
        user_id (int): ID of the user to update
        user (UserUpdate): Updated user data
        db (Session): Database session dependency
    
    Returns:
        User: Updated user information
    
    Raises:
        HTTPException: If user is not found or if email/username is already taken
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check email uniqueness if being updated
    if user.email and user.email != db_user.email:
        existing_user = db.query(models.User).filter(
            models.User.email == user.email
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check username uniqueness if being updated
    if user.username and user.username != db_user.username:
        existing_user = db.query(models.User).filter(
            models.User.username == user.username
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    """Delete a user.
    
    Args:
        user_id (int): ID of the user to delete
        db (Session): Database session dependency
    
    Raises:
        HTTPException: If user is not found
    
    Returns:
        None
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(db_user)
    db.commit()
    return None 