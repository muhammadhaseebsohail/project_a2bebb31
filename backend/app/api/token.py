To test the authentication API, we will use the built-in FastAPI test client and pytest. To illustrate the testing of authentication endpoints, we will consider simple login and signup endpoints. Let's start by writing the FastAPI application.

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def authenticate_user(fake_db, username: str, password: str):
    # Implement your authentication logic here
    pass

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}
```

Now, let's write our unit tests for these endpoints.

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_token():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["access_token"]
    assert "token_type" in token
    assert token["token_type"] == "bearer"

def test_get_token_invalid_user():
    response = client.post(
        "/token",
        data={"username": "invalid", "password": "invalid"}
    )
    assert response.status_code == 401
```

To run these tests, you would use a command like:

```bash
pytest test_main.py
```

Please note that the provided code does not implement the `authenticate_user` method or a user database. In a real-world application, you would need to handle user authentication, storing user data securely, and generating tokens properly. You may use libraries like Passlib for password hashing and SQLAlchemy for database operations. In your tests, you should create fake user data in your setup method and remove it in your teardown method.