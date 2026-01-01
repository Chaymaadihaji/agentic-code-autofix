python
# main.py
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from bson import ObjectId
import uvicorn
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Union

# Définition des constantes
SECRET_KEY = "1f23b4c5c56d7e8f9g10a11b12c13d14"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Définition de la modèle utilisateur
class User(BaseModel):
    id: str
    email: str
    password: str

# Définition de l'API
app = FastAPI(title="API REST en Python avec FastAPI et MongoDB")

# Configuration de CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion à la base de données MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["api_rest"]
collection = db["utilisateurs"]

# Définition de la fonction de hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

# Définition de la fonction de génération de tokens JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Définition de la fonction de vérification des tokens JWT
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username == None:
            raise credentials_exception
        token_data = User(id=username)
    except JWTError:
        raise credentials_exception
    return token_data

# Définition des routes API
@app.get("/api")
async def fonctionnalite_principale():
    try:
        return JSONResponse(content={"message": "API REST en Python avec FastAPI et MongoDB"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Route de connexion utilisateur
@app.post("/api/login")
async def login_for acces_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=401, detail="L'email n'est pas reconnu")
    pwd = pwd_context.verify(form_data.password, user["password"])
    if not pwd:
        raise HTTPException(status_code=401, detail="Le mot de passe est incorrect")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)

# Route de vérification de token
@app.get("/api/token")
def read_token():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Le token n'est pas fourni ou est vide")
    token = token.removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_data = User(id=username)
        return JSONResponse(content={"user": token_data}, status_code=200)
    except JWTError:
        raise HTTPException(status_code=401, detail="Le token est invalide")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
