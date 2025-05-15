To test our FastAPI application, we can use the `TestClient` provided by FastAPI. It uses `requests` internally and provides a simple way to simulate HTTP requests to our application in our tests.

First, let's add our necessary imports:

```python
from fastapi.testclient import TestClient
import pytest
from main import app, UserBase, get_password_hash, create_access_token
```

Here, `main` is the Python file where our FastAPI application is defined.

Now, we can initialize the `TestClient`:

```python
client = TestClient(app)
```

We will also need some test data:

```python
test_user = {
    "username": "testuser",
    "hashed_password": get_password_hash("testpassword"),
}
```

Now we can write our tests. Let's start with a success case:

```python
def test_login_success():
    response = client.post(
        "/token",
        data={
            "username": test_user["username"],
            "password": "testpassword"
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
```

We can also test for an error case, such as invalid credentials:

```python
def test_login_error():
    response = client.post(
        "/token",
        data={
            "username": test_user["username"],
            "password": "wrongpassword"
        },
    )
    assert response.status_code == 401
```

We should also test our data validation. For example, our `UserBase` model specifies that the `username` field must be between 3 and 50 characters. We can test that this validation is working correctly:

```python
def test_login_username_too_short():
    response = client.post(
        "/token",
        data={
            "username": "ab",
            "password": "testpassword"
        },
    )
    assert response.status_code == 422

def test_login_username_too_long():
    response = client.post(
        "/token",
        data={
            "username": "a" * 51,
            "password": "testpassword"
        },
    )
    assert response.status_code == 422
```

Because JWT tokens are stateless, there's not much we can do to test the logout endpoint. However, we can at least test that it's returning a 200 status code:

```python
def test_logout():
    response = client.post(
        "/logout",
        headers={"Authorization": f"Bearer {create_access_token(data={'sub': test_user['username']})}"},
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Logged out"}
```

We are assuming here that the `create_access_token` function creates a valid JWT token. If this is not the case, this test may fail.