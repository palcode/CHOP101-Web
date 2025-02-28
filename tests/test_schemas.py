import pytest
from pydantic import ValidationError
from app.schemas import UserCreate, UserUpdate, User
from datetime import datetime

def test_user_create_valid():
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "street_address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "postal_code": "12345"
    }
    user = UserCreate(**user_data)
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.password == user_data["password"]
    assert user.street_address == user_data["street_address"]

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="invalid-email",
            username="testuser",
            password="password123",
            street_address="123 Test St",
            city="Test City",
            state="TS",
            country="Test Country",
            postal_code="12345"
        )

def test_user_create_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@example.com",
            username="testuser",
            password="short",
            street_address="123 Test St",
            city="Test City",
            state="TS",
            country="Test Country",
            postal_code="12345"
        )

def test_user_update_partial():
    update_data = {
        "email": "updated@example.com",
        "street_address": "New Address"
    }
    user_update = UserUpdate(**update_data)
    assert user_update.email == update_data["email"]
    assert user_update.street_address == update_data["street_address"]
    assert user_update.username is None
    assert user_update.password is None

def test_user_update_invalid_email():
    with pytest.raises(ValidationError):
        UserUpdate(email="invalid-email")

def test_user_model_complete():
    user_data = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "street_address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "postal_code": "12345",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    user = User(**user_data)
    assert user.id == user_data["id"]
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.is_active == user_data["is_active"]
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime) 