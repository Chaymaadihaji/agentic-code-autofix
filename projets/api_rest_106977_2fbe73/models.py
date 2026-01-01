python
# models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CORS_ALLOWED_ORIGIN = ["*"]
CORS_ALLOWED_METHODS = ["*"]
CORS_ALLOWED_HEADERS = ["*"]

# Define the database model
frommotor import MotorClient

client = MotorClient("mongodb://localhost:27017")

db = client["api_database"]
collection = db["users"]

class User(BaseModel):
    """User model"""
    id: Optional[str] = None
    username: str
    email: str
    password: str

    class Config:
        anystr_strip_whitespace = True

def get_password_hash(password: str):
    """Hash a password"""
    pwd_context = CryptContext(
        schemes=["pbkdf2SHA256"],
        default="pbkdf2SHA256",
        pbkdf2_sha256__min_rounds=20000,
    )

    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """Verify a password"""
    pwd_context = CryptContext(
        schemes=["pbkdf2SHA256"],
        default="pbkdf2SHA256",
        pbkdf2_sha256__min_rounds=20000,
    )

    return pwd_context.verify(plain_password, hashed_password)

class PyObjectId(BaseModel):
    """PyObjectId model"""
    def __init__(self, value: Optional[str] = None):
        self.id = str(value)  # Store it as string
        if value is not None:
            try:
                PydanticObjectId(value)
            except ValidationError:
                raise ValueError("invalid ObjectId")
class PyObjectBase BaseModel):
    id: PyObjectId = PyObjectId(None)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class ItemBase(BaseModel):
    title: str | None = None
    description: str | None = None

class Item(ItemBase):
    id: PyObjectId = PyObjectId(None)
    user_id: PyObjectId = PyObjectId(None)

    class Config:
        anystr_strip_whitespace = True

class ItemCreate(ItemBase):
    pass
