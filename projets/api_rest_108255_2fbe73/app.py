python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jwt import DecodeError, MissingRequiredClaimError, ExpiredSignatureError
from typing import Optional
from pymongo import MongoClient

# Configuration
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MONGO_URI = "mongodb://localhost:27017/"

# Création de l'application
app = FastAPI(title="API REST avec FastAPI et MongoDB",
                description="Cette application est une API REST utilisant FastAPI et MongoDB.",
                version="4.0")

# Configuration de l'authentification
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

# Création du modèle de données pour l'utilisateur
class Utilisateur(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str

# Fonction pour la vérification des mots de passe
def verifier_mdp( hashed_password: str, mot_de_passe: str):
    try:
        return pwd_context.verify(mot_de_passe, hashed_password)
    except:
        return False

# Fonction pour l'encodage du jeton
def encode_token(data: dict):
    return f"Bearer {jwt.encode(data, SECRET_KEY, ALGORITHM)}"

# Fonction pour la vérification du jeton
def verify_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# Création du client pour MongoDB
client = MongoClient(MONGO_URI)

def get_collection():
    db = client['database']
    collection = db['utilisateurs']
    return collection

# Fonction pour insérer un utilisateur
@app.post("/insérer_utilisateur/")
async def insérer_utilisateur(utilisateur: Utilisateur):
    collection = get_collection()
    utilisateur_dict = utilisateur.dict()
    collection.insert_one(utilisateur_dict)
    return {"message": "Utilisateur inséré"}

# Fonction pour récuperer les utilisateurs
@app.get("/utilisateurs/")
async def récuperer_utilisateurs():
    collection = get_collection()
    utilisateurs = collection.find()
    return [{"id": utilisateur["id"], "username": utilisateur["username"], "email": utilisateur["email"]} for utilisateur in utilisateurs]

# Fonction pour obtenir un jeton d'authentification
@app.post("/obtenir_jetons/")
async def obtenir_jetons(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        utilisateur = Utilisateur.get_utilisateur(form_data.login)
        if utilisateur and pwd_context.verify(form_data.password, utilisateur.hashed_password):
            utilisateur_dict = utilisateur.dict()
            utilisateur_dict.pop("hashed_password")
            token_expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = jwt.encode({"exp": int(token_expires_at.timestamp()),
                                "iat": int(datetime.utcnow().timestamp()),
                                "sub": utilisateur_dict['id'],
                                "username": utilisateur_dict['username'],
                                "email": utilisateur_dict['email']},
                               SECRET_KEY, ALGORITHM)
            return {"access_token": token, "token_type": "bearer"}
        raise HTTPException(status_code=401, detail="Authentication failed")
    except:
        raise HTTPException(status_code=500, detail="Erreur de base de données")

async def get_current_active_user(
    token: str = Depends(
        HTTPBearer(schemename="Bearer")
    )
):
    return Utilisateur()

# Route pour les requêtes GET
@app.get("/protected")
async def protected_route(current_user: Utilisateur):
    return {"message": f"Bonjour {current_user.username} !"}

# Configuration CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import jwt
