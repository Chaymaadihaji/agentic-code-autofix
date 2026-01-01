python
# Importation des modules nécessaires
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta

# Définition des Constantes
SECRET_KEY = "d5a7f0e2b6c9a8f7e5d3c2b1a0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_HOURS = 24

# Configuration MongoDB
MongoClient = 'mongodb://localhost:27017/'
DB_NAME = 'mydatabase'
COLLECTION_NAME = 'mycollection'

# Création de l'application FastAPI
app = FastAPI(
    title="Mon API avec FastAPI",
    description="API REST créée avec FastAPI et MongoDB",
    version="1.0",
    terms_of_service="https://www.example.com/policies/terms/",
    contact={
        "name": "Jean Doe",
        "email": "jean.doe@example.com",
        "url": "https://www.example.com/about/contact/",
    },
    license={
        "name": "License: MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    dependencies=[Depends(get_db)],
)

# Définition d'un modèle de données
class User(BaseModel):
    id: int
    email: EmailStr

class Post(BaseModel):
    user_id: int
    title: str
    content: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# Définition d'un espace de travail pour MongoDB
from pymongo import MongoClient

client = MongoClient(MongoClient)
db = client[DB_NAME]
users = db[COLLECTION_NAME]

# Fonctions helpers
def get_db():
    while True:
        db = client[DB_NAME]
        db_user = db[COLLECTION_NAME].find_one({'email': "user1@example.com"})
        if db_user:
            yield db, db_user

def verify_password(plain_password, hashed_password):
    return CryptContext(schemes=["bcrypt"], default="bcrypt").verify(plain_password, hashed_password)

def authenticate_user(user_db, user_credentials):
    if (user_db["password"]) == (authenticate(user_credentials["password"])):
        return db_user
    return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_password_hash(password: str):
    return CryptContext(schemes=["bcrypt"], default="bcrypt").hash(password)

# Définition d'une fonction pour générer un token d'accès JWT
async def token_authentication(token: str = Depends()):
    from jose import jwt
    from datetime import datetime, timedelta

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Token non valide")

    if data['exp'] < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Token expiré")

    return data

# Définition d'une fonction pour la recherche de données
async def get_user(id: int):
    try:
        user = users.find_one({"id": id})
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Définition des routes de notre API
@app.get("/user/{user_id}", response_model=UserSchema)
def read_user(user_id: int, token: str = Depends(token_authentication)):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@app.post("/post", response_model=Post, description="Créer une nouvelle publication")
async def create_post(form_data: Post = Form(description="Formulaire de publication")):
    await users.insert_one(form_data)
    return form_data

@app.get("/token", response_model=UserSchema)
async def login_for_access_token(username: str = Form("username"), password: str = Form("password")):
    user_db = db_user
    if not user_db:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    if not verify_password(password, user_db["password"]):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRES_HOURS)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
