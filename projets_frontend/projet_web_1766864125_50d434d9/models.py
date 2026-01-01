# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from flask import Flask
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)

class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)
    date_emprunt = db.Column(db.DateTime, nullable=False)
    date_retour = db.Column(db.DateTime, nullable=False)

class ApiLivre(Resource):
    def get(self):
        livres = Livre.query.all()
        return [{'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur} for livre in livres]

class ApiMembre(Resource):
    def get(self):
        membres = Membre.query.all()
        return [{'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom, 'email': membre.email} for membre in membres]

class ApiEmprunt(Resource):
    def get(self):
        emprunts = Emprunt.query.all()
        return [{'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id, 'date_emprunt': emprunt.date_emprunt, 'date_retour': emprunt.date_retour} for emprunt in emprunts]

class ApiAuth(Resource):
    def post(self):
        data = request.get_json()
        if data['email'] == 'admin' and data['password'] == 'admin':
            access_token = jwt.create_access_token(identity=data['email'])
            return {'access_token': access_token}
        return {'error': 'Invalid credentials'}, 401

api.add_resource(ApiLivre, '/livres')
api.add_resource(ApiMembre, '/membres')
api.add_resource(ApiEmprunt, '/emprunts')
api.add_resource(ApiAuth, '/auth')

@app.route('/')
def index():
    return 'Bienvenue dans la bibliothèque !'

if __name__ == "__main__":
    app.run(debug=True)
