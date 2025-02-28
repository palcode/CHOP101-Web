"""Database configuration module for the FastAPI User Management API.

This module sets up the SQLAlchemy database connection and session management.
It provides the database engine, session factory, and dependency injection for database sessions.

Attributes:
    SQLALCHEMY_DATABASE_URL (str): The SQLite database URL
    engine: SQLAlchemy database engine instance
    SessionLocal: SQLAlchemy session factory
    Base: SQLAlchemy declarative base class
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Database session dependency.
    
    Creates a new database session for each request and ensures proper cleanup.
    
    Yields:
        Session: SQLAlchemy database session
    
    Example:
        @app.get("/users/")
        def read_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 