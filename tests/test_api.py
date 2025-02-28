import pytest
from fastapi import status

def test_create_user_success(client, sample_user_data):
    response = client.post("/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["username"] == sample_user_data["username"]
    assert data["street_address"] == sample_user_data["street_address"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data

def test_create_user_duplicate_email(client, created_user, sample_user_data):
    response = client.post("/users/", json=sample_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"

def test_create_user_duplicate_username(client, created_user):
    new_user_data = {
        "email": "another@example.com",
        "username": "testuser",  # Same username as created_user
        "password": "password123",
        "street_address": "456 Test St",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "postal_code": "12345"
    }
    response = client.post("/users/", json=new_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already taken"

def test_create_user_invalid_password(client):
    invalid_user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "short",  # Less than 8 characters
        "street_address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "postal_code": "12345"
    }
    response = client.post("/users/", json=invalid_user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_users_empty(client):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_users_with_data(client, created_user):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) == 1
    assert users[0]["email"] == created_user["email"]

def test_get_users_with_filters(client, created_user):
    # Test city filter
    response = client.get(f"/users/?city={created_user['city']}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

    # Test with non-existent city
    response = client.get("/users/?city=NonExistentCity")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0

def test_get_user_by_id(client, created_user):
    response = client.get(f"/users/{created_user['id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == created_user

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

def test_update_user_success(client, created_user):
    update_data = {
        "email": "updated@example.com",
        "street_address": "Updated Address"
    }
    response = client.put(f"/users/{created_user['id']}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    updated_user = response.json()
    assert updated_user["email"] == update_data["email"]
    assert updated_user["street_address"] == update_data["street_address"]
    assert updated_user["username"] == created_user["username"]  # Unchanged field

def test_update_user_not_found(client):
    response = client.put("/users/999", json={"email": "test@example.com"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_user_duplicate_email(client, created_user):
    # Create another user first
    another_user = {
        "email": "another@example.com",
        "username": "anotheruser",
        "password": "password123",
        "street_address": "456 Test St",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "postal_code": "12345"
    }
    client.post("/users/", json=another_user)
    
    # Try to update first user with second user's email
    response = client.put(
        f"/users/{created_user['id']}", 
        json={"email": "another@example.com"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"

def test_delete_user_success(client, created_user):
    response = client.delete(f"/users/{created_user['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify user is deleted
    get_response = client.get(f"/users/{created_user['id']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND 