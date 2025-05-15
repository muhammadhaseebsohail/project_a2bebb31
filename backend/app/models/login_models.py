You have done a good job of providing the necessary Pydantic models, service layer code, and API endpoint. However, to complete your task, we need to define the `create_access_token` function that you mentioned, and we need to adjust the `LoginResponse` model to include the `token_type` field. Moreover, the `get_user` function is not defined, so let's do that as well. Here is the complete code:

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, Field, validator
from typing import Optional
import re
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Pydantic models
class LoginForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)

    @validator('password')
    def password_strength(cls, v):
        if not re.findall(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.findall('[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class LoginResponse(BaseModel):
    username: str
    access_token: Optional[str]
    token_type: Optional[str]
    detail: Optional[str]

# Service layer
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(fake_db, username: str):
    # Here we're assuming 'fake_db' is a dictionary mapping usernames to user data
    if username in fake_db:
        user_dict = fake_db[username]
        return user_dict

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# FastAPI endpoint
@app.post('/login', response_model=LoginResponse)
async def login(form_data: LoginForm):
    """
    Endpoint to handle user login
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
```

This code includes everything you need for your login endpoint, including the necessary imports, Pydantic models for request and response, service layer code, and the FastAPI endpoint. Make sure to replace `"YOUR_SECRET_KEY"` with your actual secret key.