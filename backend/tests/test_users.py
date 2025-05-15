Here's how you might write the tests for this FastAPI application using pytest and FastAPI's TestClient:

```python
import pytest
from fastapi.testclient import TestClient
from main import app, get_db, UserCreate
from sqlalchemy.orm import Session

# Mock the dependency
def override_get_db():
    db = SessionLocal()
    return db

app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture
def test_user():
    return UserCreate(username="testuser", password="testpass")


# Test creating a user
def test_create_user(test_user):
    response = client.post("/users/", json=test_user.dict())
    assert response.status_code == 201, "Expected status code 201"
    data = response.json()
    assert "id" in data, "Expected id in response"
    assert data["username"] == test_user.username, "Expected same username in response"
    assert "password" not in data, "Did not expect password in response"


# Test creating a user with an existing username
def test_create_user_existing_username(test_user):
    client.post("/users/", json=test_user.dict())  # create user first
    response = client.post("/users/", json=test_user.dict())
    assert response.status_code == 400, "Expected status code 400"
    assert response.json() == {"detail": "Username already exists"}, "Expected error detail message"


# Test getting a user
def test_get_user(test_user):
    response = client.post("/users/", json=test_user.dict())
    id = response.json()["id"]
    response = client.get(f"/users/{id}")
    assert response.status_code == 200, "Expected status code 200"
    data = response.json()
    assert data["id"] == id, "Expected same id in response"
    assert data["username"] == test_user.username, "Expected same username in response"


# Test getting a user that does not exist
def test_get_user_not_exist():
    response = client.get("/users/9999")
    assert response.status_code == 404, "Expected status code 404"
    assert response.json() == {"detail": "User not found"}, "Expected error detail message"


# Test creating a user with invalid data
def test_create_user_invalid_data():
    response = client.post("/users/", json={"username": "testuser"})
    assert response.status_code == 422, "Expected status code 422"
    assert "detail" in response.json(), "Expected detail in response"
``` 

In these tests, we first override the `get_db` dependency to return a session from our test database. Then we define a pytest fixture for a test user, and use this fixture in our tests. We test both success and error cases, and we also test data validation by trying to create a user with invalid data. If any of these tests fail, the assert statements will raise an AssertionError with a helpful message.