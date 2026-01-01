python
# app.py

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId

app = FastAPI(title="Mon API",
              description="API REST avec FastAPI et MongoDB",
              version="1.0",
              contact={"name": "Toto", "email": "toto@example.com"},)

# Configurations
SECRET_KEY = "secreteeeftrt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Authentification JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return dict(payload)
    except JWTError:
        return None

def get_current_active_user(current_user: str = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return current_user

# Modèle de données
class Utilisateur(BaseModel):
    id_utilisateur : Optional[str]
    username: str
    password: str

# Chemin MongoDB
client = MongoClient("mongodb://localhost:27017/")
database = client["mydatabase"]
collection = database["utilisateurs"]

# Sécurité
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

# Documentation Swagger
api_v1_tag = {
    "name": "Utilisateurs",
    "description": "Opérations relatives aux utilisateurs"
}

@app.get("/users/", response_model=list[Utilisateur], tags=["Utilisateurs"])
async def read_users():
    users = list(collection.find({}, {"_id": False}))
    return users

@app.post("/users/", response_model=Utilisateur, tags=["Utilisateurs"])
async def create_user(user: Utilisateur):
    collection.insert_one(user.dict())
    return user

@app.get("/users/{id_utilisateur}", response_model=Utilisateur, tags=["Utilisateurs"])
async def read_user(id_utilisateur: str):
    user = list(collection.find({"id_utilisateur": id_utilisateur}, {"_id": False}))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]

@app.patch("/users/{id_utilisateur}", response_model=Utilisateur, tags=["Utilisateurs"])
async def update_user(id_utilisateur: str, user: Utilisateur):
    collection.update_one({"id_utilisateur": id_utilisateur}, {"$set": user.dict()})
    return user

@app.delete("/users/{id_utilisateur}", response_model=dict, tags=["Utilisateurs"])
async def delete_user(id_utilisateur: str):
    collection.delete_one({"id_utilisateur": id_utilisateur})
    return {"message": "User deleted"}

# Authentification
@app.post("/auth")
async def auth_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = list(collection.find({"username": form_data.username, "password": form_data.password}, {"_id": False}))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode({"sub": user[0]["id_utilisateur"], "exp": access_token_expires}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

# Gestion d'exceptions
@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc}})
