python
# models.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, Request

app = FastAPI(
    title="API",
    description="API REST avec FastAPI et MongoDB",
    version="1.0",
    openapi_tags=[{"name":"autres","description":"Touts les endpoints autres"}],
)

# Configuration JWT
secret_key = "secret_key"
algorithm = "HS256"
expiration_time = 60 * 15  # 15 minutes

# Création d'un contexte de hachage pour le mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

# Classe de modèle de données MongoDB
Base = declarative_base()

class UserMongoDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    create_at = Column(DateTime)


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


# Création d'un endpoint d'inscription
@app.post("/inscription")
async def inscription(request: Request, user: UserMongoDB):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    Base.session.add(user)
    Base.session.commit()
    return JSONResponse(status_code=202, content={"message": "L'utilisateur a été créé avec succès"})

# Création d'un endpoint d'identification
@app.post("/login")
async def login(request: Request, user: UserMongoDB):
    if not user or not user.password:
        return JSONResponse(status_code=401, content={"message": "Informations manquantes"})
    try:
        hashed_password = pwd_context.verify(user.password, user.password)
        if not hashed_password:
            raise ValueError
        access_token = jwt.encode({"sub": user.login}, secret_key, algorithm)
        return JSONResponse(status_code=200, content={"access_token": access_token, "token_type": "bearer"})
    except ValueError:
        return JSONResponse(status_code=401, content={"message": "Mot de passe incorrect"})

# Gestion des exceptions
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "Une erreur inconnue est survenue"})
