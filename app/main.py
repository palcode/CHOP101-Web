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

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas, database
from typing import List, Optional
from passlib.context import CryptContext
import time
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    handlers=[RotatingFileHandler('app.log', maxBytes=100000, backupCount=5)],
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create tables
try:
    models.Base.metadata.create_all(bind=database.engine)
except SQLAlchemyError as e:
    logger.error(f"Failed to create database tables: {str(e)}")
    raise

app = FastAPI(
    title="User Management API",
    description="API for managing users with address information",
    version="1.0.0",
    docs_url="/api/docs",  # Change Swagger UI path
    redoc_url="/api/redoc"  # Change ReDoc path
)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting
RATE_LIMIT_DURATION = timedelta(minutes=1)
MAX_REQUESTS = 100
request_history = {}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Middleware for rate limiting and logging
@app.middleware("http")
async def middleware(request: Request, call_next):
    # Rate limiting
    client_ip = request.client.host
    current_time = datetime.now()
    
    if client_ip in request_history:
        request_times = request_history[client_ip]
        # Remove old requests
        request_times = [t for t in request_times 
                        if current_time - t < RATE_LIMIT_DURATION]
        
        if len(request_times) >= MAX_REQUESTS:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )
        
        request_times.append(current_time)
        request_history[client_ip] = request_times
    else:
        request_history[client_ip] = [current_time]
    
    # Request logging
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {process_time:.3f}s"
    )
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

# Error handler for database errors
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# CRUD Operations
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db)
):
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
    try:
        # Check if email exists
        if db.query(models.User).filter(
            models.User.email == user.email
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username exists
        if db.query(models.User).filter(
            models.User.username == user.username
        ).first():
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
        
        logger.info(f"Created new user with email: {user.email}")
        return db_user
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

@app.get("/users/", response_model=List[schemas.User])
async def read_users(
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
    try:
        # Validate pagination parameters
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip value must be non-negative"
            )
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 100"
            )
        
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
        
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(database.get_db)):
    """Retrieve a specific user by ID.
    
    Args:
        user_id (int): ID of the user to retrieve
        db (Session): Database session dependency
    
    Returns:
        User: User information
    
    Raises:
        HTTPException: If user is not found
    """
    try:
        if user_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user
        
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )

@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
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
    try:
        if user_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check email uniqueness if being updated
        if user.email and user.email != db_user.email:
            if db.query(models.User).filter(
                models.User.email == user.email
            ).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Check username uniqueness if being updated
        if user.username and user.username != db_user.username:
            if db.query(models.User).filter(
                models.User.username == user.username
            ).first():
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
        
        logger.info(f"Updated user {user_id}")
        return db_user
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while updating user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    """Delete a user.
    
    Args:
        user_id (int): ID of the user to delete
        db (Session): Database session dependency
    
    Raises:
        HTTPException: If user is not found
    
    Returns:
        None
    """
    try:
        if user_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
        
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(db_user)
        db.commit()
        
        logger.info(f"Deleted user {user_id}")
        return None
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while deleting user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        ) 