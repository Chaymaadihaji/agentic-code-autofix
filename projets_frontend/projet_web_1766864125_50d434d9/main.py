from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restful import Api, Resource
from streamlit import st
from streamlit.components.v1 import iframe
from fpdf import FPDF
import json
import uuid
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)

class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)
    date_emprunt = db.Column(db.DateTime, nullable=False)
    date_retour = db.Column(db.DateTime, nullable=False)

class Login(Resource):
    def post(self):
        email = request.json['email']
        mot_de_passe = request.json['mot_de_passe']
        membre = Membre.query.filter_by(email=email).first()
        if membre and membre.mot_de_passe == mot_de_passe:
            access_token = create_access_token(identity=membre.id)
            return jsonify(access_token=access_token)
        return jsonify(error='Membre non trouvé ou mot de passe incorrect'), 401

class Livres(Resource):
    @jwt_required
    def get(self):
        livres = Livre.query.all()
        return [{'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur, 'isbn': livre.isbn} for livre in livres]

class Membres(Resource):
    @jwt_required
    def get(self):
        membres = Membre.query.all()
        return [{'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom, 'email': membre.email} for membre in membres]

class Emprunts(Resource):
    @jwt_required
    def get(self):
        emprunts = Emprunt.query.all()
        return [{'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id, 'date_emprunt': emprunt.date_emprunt, 'date_retour': emprunt.date_retour} for emprunt in emprunts]

class API(Resource):
    @jwt_required
    def post(self):
        data = request.json
        livre = Livre.query.get(data['livre_id'])
        membre = Membre.query.get(data['membre_id'])
        if livre and membre:
            emprunt = Emprunt(livre_id=livre.id, membre_id=membre.id, date_emprunt=data['date_emprunt'], date_retour=data['date_retour'])
            db.session.add(emprunt)
            db.session.commit()
            return jsonify({'message': 'Emprunt créé'})
        return jsonify({'error': 'Livres ou membres non trouvés'}), 400

class PDF(Resource):
    @jwt_required
    def get(self):
        emprunts = Emprunt.query.all()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=15)
        pdf.cell(200, 10, txt='Emprunts', ln=True, align='C')
        pdf.ln(10)
        for emprunt in emprunts:
            pdf.cell(200, 10, txt=f'Livre {emprunt.livre_id} - Membre {emprunt.membre_id} - Date emprunt {emprunt.date_emprunt} - Date retour {emprunt.date_retour}', ln=True, align='L')
        pdf.output('emprunts.pdf')
        return jsonify({'message': 'PDF créé'})

api.add_resource(Login, '/login')
api.add_resource(Livres, '/livres')
api.add_resource(Membres, '/membres')
api.add_resource(Emprunts, '/emprunts')
api.add_resource(API, '/api')
api.add_resource(PDF, '/pdf')

@app.route('/')
def index():
    return st.title('Bibliothèque')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
