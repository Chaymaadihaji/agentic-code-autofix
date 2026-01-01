import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
import pytz
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['JWT_SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    editeur = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)
    date_emprunt = db.Column(db.DateTime, nullable=False)
    date_retour = db.Column(db.DateTime, nullable=False)

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    mot_de_passe = request.json['mot_de_passe']
    membre = Membre.query.filter_by(email=email).first()
    if membre and check_password_hash(mot_de_passe, membre.mot_de_passe):
        access_token = create_access_token(identity=membre.id)
        return jsonify(access_token=access_token)
    return jsonify({'error': 'Mauvais email ou mot de passe'}), 401

@app.route('/livres', methods=['GET'])
@jwt_required
def get_livres():
    livres = Livre.query.all()
    return jsonify([{'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur, 'editeur': livre.editeur, 'stock': livre.stock} for livre in livres])

@app.route('/livres', methods=['POST'])
@jwt_required
def create_livre():
    titre = request.json['titre']
    auteur = request.json['auteur']
    editeur = request.json['editeur']
    stock = request.json['stock']
    livre = Livre(titre=titre, auteur=auteur, editeur=editeur, stock=stock)
    db.session.add(livre)
    db.session.commit()
    return jsonify({'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur, 'editeur': livre.editeur, 'stock': livre.stock})

@app.route('/livres/<int:livre_id>', methods=['PUT'])
@jwt_required
def update_livre(livre_id):
    livre = Livre.query.get(livre_id)
    titre = request.json['titre']
    auteur = request.json['auteur']
    editeur = request.json['editeur']
    stock = request.json['stock']
    livre.titre = titre
    livre.auteur = auteur
    livre.editeur = editeur
    livre.stock = stock
    db.session.commit()
    return jsonify({'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur, 'editeur': livre.editeur, 'stock': livre.stock})

@app.route('/livres/<int:livre_id>', methods=['DELETE'])
@jwt_required
def delete_livre(livre_id):
    livre = Livre.query.get(livre_id)
    db.session.delete(livre)
    db.session.commit()
    return jsonify({'message': 'Livre supprimé'})

@app.route('/membres', methods=['GET'])
@jwt_required
def get_membres():
    membres = Membre.query.all()
    return jsonify([{'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom, 'email': membre.email} for membre in membres])

@app.route('/membres', methods=['POST'])
@jwt_required
def create_membre():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    mot_de_passe = generate_password_hash(request.json['mot_de_passe'])
    membre = Membre(nom=nom, prenom=prenom, email=email, mot_de_passe=mot_de_passe)
    db.session.add(membre)
    db.session.commit()
    return jsonify({'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom, 'email': membre.email})

@app.route('/membres/<int:membre_id>', methods=['PUT'])
@jwt_required
def update_membre(membre_id):
    membre = Membre.query.get(membre_id)
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    mot_de_passe = generate_password_hash(request.json['mot_de_passe'])
    membre.nom = nom
    membre.prenom = prenom
    membre.email = email
    membre.mot_de_passe = mot_de_passe
    db.session.commit()
    return jsonify({'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom, 'email': membre.email})

@app.route('/membres/<int:membre_id>', methods=['DELETE'])
@jwt_required
def delete_membre(membre_id):
    membre = Membre.query.get(membre_id)
    db.session.delete(membre)
    db.session.commit()
    return jsonify({'message': 'Membre supprimé'})

@app.route('/emprunts', methods=['GET'])
@jwt_required
def get_emprunts():
    emprunts = Emprunt.query.all()
    return jsonify([{'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id, 'date_emprunt': emprunt.date_emprunt, 'date_retour': emprunt.date_retour} for emprunt in emprunts])

@app.route('/emprunts', methods=['POST'])
@jwt_required
def create_emprunt():
    livre_id = request.json['livre_id']
    membre_id = request.json['membre_id']
    date_emprunt = datetime.now(pytz.utc)
    date_retour = date_emprunt + datetime.timedelta(days=14)
    emprunt = Emprunt(livre_id=livre_id, membre_id=membre_id, date_emprunt=date_emprunt, date_retour=date_retour)
    db.session.add(emprunt)
    db.session.commit()
    return jsonify({'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id, 'date_emprunt': emprunt.date_emprunt, 'date_retour': emprunt.date_retour})

@app.route('/emprunts/<int:emprunt_id>', methods=['PUT'])
@jwt_required
def update_emprunt(emprunt_id):
    emprunt = Emprunt.query.get(emprunt_id)
    livre_id = request.json['livre_id']
    membre_id = request.json['membre_id']
    date_emprunt = request.json['date_emprunt']
    date_retour = request.json['date_retour']
    emprunt.livre_id = livre_id
    emprunt.membre_id = membre_id
    emprunt.date_emprunt = date_emprunt
    emprunt.date_retour = date_retour
    db.session.commit()
    return jsonify({'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id, 'date_emprunt': emprunt.date_emprunt, 'date_retour': emprunt.date_retour})

@app.route('/emprunts/<int:emprunt_id>', methods=['DELETE'])
@jwt_required
def delete_emprunt(emprunt_id):
    emprunt = Emprunt.query.get(emprunt_id)
    db.session.delete(emprunt)
    db.session.commit()
    return jsonify({'message': 'Emprunt supprimé'})

@app.route('/rapport', methods=['GET'])
@jwt_required
def generer_rapport():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Rapport bibliothèque", ln=True, align='C')
    pdf.output("rapport.pdf")
    return jsonify({'message': 'Rapport généré'})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
