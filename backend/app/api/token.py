Here is an example of how you can set up a secure session storage API in FastAPI:

1. The complete endpoint code with all imports:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import uvicorn

app = FastAPI()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate user here (omitted for brevity)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

2. Pydantic models for request/response:

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

3. Any necessary service layer code:

In the above code, the service layer is the function `create_access_token()`. This function is responsible for generating the JWT token. 

The `login_for_access_token()` function is the endpoint for the client to get the access token. It validates the user (omitted for brevity) and uses the `create_access_token()` function to create the JWT token. The JWT token is then sent to the client.

To run the server, use:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Keep in mind that this is a basic example. In a real-world application, you would need to add more complex authentication and authorization, handle user management, etc. For simplicity, this example uses JWT for session management, but in a production environment, you may want to consider using a more secure solution like server-side sessions.