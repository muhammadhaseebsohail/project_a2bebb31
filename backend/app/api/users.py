Here's an example of how you might achieve this. First, let's create the FastAPI application and set up the database models:

```python
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Now, let's define the Pydantic models for the request and response:

```python
class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
```

Next, we define the service layer code:

```python
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

Finally, we define the endpoints:

```python
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return db_user

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by id
    """
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

In the code above, we've created a simple FastAPI application with SQLAlchemy for ORM. It connects to a SQLite database and has two endpoints: one for creating a new user and another for fetching a user by id. We use Pydantic models for data validation and transformation, and we follow RESTful principles. Note that in a real-world scenario, you would never store passwords in plain text. Always hash and salt passwords before storing them in your database.