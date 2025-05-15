First, let's define our Pydantic models for the request and response:

```python
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserInDB(UserBase):
    hashed_password: str

class TokenData(BaseModel):
    username: str = None
```
Now, let's implement the service layer to perform the necessary operations:

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```
Finally, let's create the FastAPI endpoints for login and logout:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=TokenData)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User login endpoint, verifies provided username and password, and returns JWT token.
    """
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout(current_user: str = Depends(oauth2_scheme)):
    """
    User logout endpoint, the current logged in user is logged out.
    """
    return {"detail": "Logged out"}
```

Please replace `fake_db` and `get_user` with your actual database and user fetching method, respectively. Also, replace `YOUR_SECRET_KEY` with your own secret key. The `login_for_access_token` endpoint verifies the user credentials and returns a JWT token. The `logout` endpoint is a placeholder and doesn't actually do anything, as JWT tokens are stateless. You can implement a token blacklist if you need actual logout functionality.