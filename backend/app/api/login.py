First, let's set up our Pydantic models for our request and response:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

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
    detail: Optional[str]
```

In the LoginForm model, we have added validation to check the password's strength, ensuring it contains at least one number and one uppercase letter.

Now, let's assume we have a service layer function authenticate_user which checks the user's credentials against the database.

```python
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
```

Here verify_password function is used to check if the provided password matches the hashed password stored in the database.

Now, let's create our API endpoint:

```python
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
        # Here we are assuming that we have a function 'create_access_token' that generates a JWT token for the user.
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
```

In the login endpoint, we are taking in the LoginForm model in the request body. Then we use the authenticate_user function to verify the user's credentials. If authentication fails, we raise an HTTPException with status code 401. If it's successful, we generate an access token for the user and send it in the response.