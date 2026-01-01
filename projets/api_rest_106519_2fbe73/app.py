python
# app.py
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional
import mongoengine
from mongoengine import connect
from datetime import datetime, timedelta
import json

# Configuration MongoDB
MONGO_DB_NAME = "mondb"
MONGO_URI = "mongodb://localhost:27017/"
connect(host=MONGO_URI, db=MONGO_DB_NAME)

# Configuration FastAPI
app = FastAPI(
    title="Mon API",
    description="Une API REST avec authentification JWT",
    version="1.0"
)
app.add_api_doc("v1")

# Configuration OAuth2
SECRET_KEY = "monclé"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuration CORS
origins = ["http://localhost:3000"]

# Définition des requêtes
class User(BaseModel):
    """Représentation d'un utilisateur"""
    id: str
    username: str
    email: str
    is_active: bool

class Token(BaseModel):
    """Représentation du jeton"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Représentation des données du jeton"""
    username: Optional[str]

# Définition de la fonction de hashage
pwd_context = CryptContext(schemes=["PBKDF2SHA1", "PBKDF2SHA256", "PBKDF2SHA384", "PBKDF2SHA512"], default="PBKDF2SHA256")

# Gestion des requêtes
def create_user(username: str, email: str, password: str, is_active: bool):
    """Création d'un utilisateur"""
    try:
        user = User.objects.create(
            username=username,
            email=email,
            password=password,
            is_active=is_active
        )
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_user(username: str):
    """Récupération d'un utilisateur"""
    try:
        user = User.objects.get(username=username)
        return user
    except:
        return None

def get_user_by_email(email: str):
    """Récupération d'un utilisateur par adresse e-mail"""
    try:
        user = User.objects.get(email=email)
        return user
    except:
        return None

def authenticate_user(username: str, password: str):
    """Authentification d'un utilisateur"""
    try:
        user = get_user(username)
        if user and pwd_context.verify(password, user.password):
            expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = jwt.encode({"sub": user.id, "exp": expiration.timestamp()}, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": access_token, "token_type": "Bearer"}
    except:
        return None

def decode_token( token: str):
    """Décode le jeton"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None

def save_token(token: str, user_id: str):
    """Enregistrement du jeton"""
    return save(user_id, token)

def delete_token(token: str):
    """Suppression du jeton"""
    return destroy(user_id, token)

def save(user_id: str, token: str):
    """Enregistrement du jeton"""
    try:
        mongoengine.connect(host=MONGO_URI, db=MONGO_DB_NAME)
        db = mongoengine.Connection(MongoClient, host=MONGO_URI, maxPoolSize=500, tz_aware=False, connect=True, alias=MONGO_DB_NAME)
        collection = db["tokens"]
        collection.drop()
        collection = db["tokens"]
        collection.save({"user_id":user_id,"token":token})
        return True
    except Exception as e:
        return False

def destroy(user_id: str, token: str):
    """Suppression du jeton"""
    try:
        mongoengine.connect(host=MONGO_URI, db=MONGO_DB_NAME)
        db = mongoengine.Connection(MongoClient, host=MONGO_URI, maxPoolSize=500, tz_aware=False, connect=True, alias=MONGO_DB_NAME)
        collection = db["tokens"]
        collection.drop()
        collection = db["tokens"]
        collection.remove(user_id=user_id, token/token)
        return True
    except Exception as e:
        return False

# API
@app.post("/users", response_model=User)
def create_user_item(user: User, password: str, is_active: bool):
    """Création d'un utilisateur"""
    try:
        return create_user(user.username, user.email, password, is_active)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authentification d'un utilisateur et obtention d'un jeton"""
    user = authenticate_user(form_data.username, form_data.password)
    if user:
        token = authenticate(user)
        data = {"access_token":token, "token_type":"Bearer"}
        return data

# Gestion des erreurs
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Gestion d'erreurs 4xx"""
    return JSONResponse(content=str(exc), status_code=exc.status_code)
