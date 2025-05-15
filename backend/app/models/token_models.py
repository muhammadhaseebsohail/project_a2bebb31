The Pydantic models needed for the provided API code are User, Token and TokenData.

Here are the models:

```python
# models.py
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
```

Explanation:
- UserBase: It's a base model that includes the fields shared by other models.
- UserCreate: It inherits from UserBase and includes password, which is needed for creating a new user but not included in the User model that is returned by the API.
- User: It's the model used in the API for returning user details. It includes fields that should not be provided by the user like id and disabled.
- Token: It's the model used for returning authentication tokens.
- TokenData: It's a model for token data that is used internally.

In your FastAPI application, you would import these models and use them. Here's how to import and use the User and Token models:

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .models import User, Token
from typing import Optional

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

Please note that you need to implement the `authenticate_user` function and a fake_db for this code to run.