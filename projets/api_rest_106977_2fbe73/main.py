python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
import jwt

app = FastAPI()

SECRET_KEY = "secret_key_here"
ALGORITHM = "HS256"

# Connexion à MongoDB
MONGODB_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGODB_URL)
db = client["mon_app"]

class Utilisateur(BaseModel):
    id: str
    username: str
    passwordDigest: str

class UtilisateurReponse(BaseModel):
    id: str
    username: str

# Fonction de vérification d'authentification
def authenticate_user(username: str, password: str):
    try:
        utilisateur = db["utilisateurs"].find_one({"username": username})
        if utilisateur and utilisateur["passwordDigest"] == password:
            return UtilisateurReponse(**utilisateur)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return None

# Création de l'API REST
@app.post("/api/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        username = form_data.username
        password = form_data.password
        utilisateur = authenticate_user(username, password)
        if utilisateur:
            access_token = jwt.encode({"sub": utilisateur.id}, SECRET_KEY, algorithm=ALGORITHM)
            db["utilisateurs"].update_one({"_id": utilisateur.id}, {"$set": {"last_login_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/api/utilisateurs/")
def read_utilisateurs():
    try:
        utilisateurs = list(db["utilisateurs"].find())
        return {"utilisateurs": utilisateurs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
