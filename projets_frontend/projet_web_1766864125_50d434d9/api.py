import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from fpdf import FPDF
import pdfkit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['JWT_SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)

class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)
    date_emprunt = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date_retour = db.Column(db.DateTime, nullable=True)

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    membre = Membre.query.filter_by(email=email).first()
    if membre and membre.password == password:
        access_token = create_access_token(identity=membre.id)
        return jsonify(access_token=access_token)
    return jsonify(error='Mauvais email ou mot de passe'), 401

@app.route('/livres', methods=['GET'])
@jwt_required
def get_livres():
    livres = Livre.query.all()
    return jsonify([{'id': l.id, 'titre': l.titre, 'auteur': l.auteur} for l in livres])

@app.route('/livres', methods=['POST'])
@jwt_required
def add_livre():
    titre = request.json['titre']
    auteur = request.json['auteur']
    livre = Livre(titre=titre, auteur=auteur)
    db.session.add(livre)
    db.session.commit()
    return jsonify({'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur})

@app.route('/livres/<int:id>', methods=['PUT'])
@jwt_required
def update_livre(id):
    livre = Livre.query.get(id)
    if livre:
        titre = request.json['titre']
        auteur = request.json['auteur']
        livre.titre = titre
        livre.auteur = auteur
        db.session.commit()
        return jsonify({'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur})
    return jsonify(error='Livre non trouvé'), 404

@app.route('/livres/<int:id>', methods=['DELETE'])
@jwt_required
def delete_livre(id):
    livre = Livre.query.get(id)
    if livre:
        db.session.delete(livre)
        db.session.commit()
        return jsonify({'message': 'Livre supprimé'})
    return jsonify(error='Livre non trouvé'), 404

@app.route('/membres', methods=['GET'])
@jwt_required
def get_membres():
    membres = Membre.query.all()
    return jsonify([{'id': m.id, 'nom': m.nom, 'prenom': m.prenom, 'email': m.email} for m in membres])

@app.route('/membres', methods=['POST'])
@jwt_required
def add_membre():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    password = request.json['password']
    membre = Membre(nom=nom, prenom=prenom, email=email, password=password)
    db.session.add(membre)
    db.session.commit()
    return jsonify({'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom, 'email': membre.email})

@app.route('/membres/<int:id>', methods=['PUT'])
@jwt_required
def update_membre(id):
    membre = Membre.query.get(id)
    if membre:
        nom = request.json['nom']
        prenom = request.json['prenom']
        email = request.json['email']
        password = request.json['password']
        membre.nom = nom
        membre.prenom = prenom
        membre.email = email
        membre.password = password
        db.session.commit()
        return jsonify({'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom, 'email': membre.email})
    return jsonify(error='Membre non trouvé'), 404

@app.route('/membres/<int:id>', methods=['DELETE'])
@jwt_required
def delete_membre(id):
    membre = Membre.query.get(id)
    if membre:
        db.session.delete(membre)
        db.session.commit()
        return jsonify({'message': 'Membre supprimé'})
    return jsonify(error='Membre non trouvé'), 404

@app.route('/emprunts', methods=['GET'])
@jwt_required
def get_emprunts():
    emprunts = Emprunt.query.all()
    return jsonify([{'id': e.id, 'livre_id': e.livre_id, 'membre_id': e.membre_id, 'date_emprunt': e.date_emprunt, 'date_retour': e.date_retour} for e in emprunts])

@app.route('/emprunts', methods=['POST'])
@jwt_required
def add_emprunt():
    livre_id = request.json['livre_id']
    membre_id = request.json['membre_id']
    emprunt = Emprunt(livre_id=livre_id, membre_id=membre_id)
    db.session.add(emprunt)
    db.session.commit()
    return jsonify({'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id, 'date_emprunt': emprunt.date_emprunt, 'date_retour': emprunt.date_retour})

@app.route('/emprunts/<int:id>', methods=['PUT'])
@jwt_required
def update_emprunt(id):
    emprunt = Emprunt.query.get(id)
    if emprunt:
        livre_id = request.json['livre_id']
        membre_id = request.json['membre_id']
        emprunt.livre_id = livre_id
        emprunt.membre_id = membre_id
        db.session.commit()
        return jsonify({'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id, 'date_emprunt': emprunt.date_emprunt, 'date_retour': emprunt.date_retour})
    return jsonify(error='Emprunt non trouvé'), 404

@app.route('/emprunts/<int:id>', methods=['DELETE'])
@jwt_required
def delete_emprunt(id):
    emprunt = Emprunt.query.get(id)
    if emprunt:
        db.session.delete(emprunt)
        db.session.commit()
        return jsonify({'message': 'Emprunt supprimé'})
    return jsonify(error='Emprunt non trouvé'), 404

@app.route('/rapport', methods=['GET'])
@jwt_required
def get_rapport():
    livres = Livre.query.all()
    membres = Membre.query.all()
    emprunts = Emprunt.query.all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Rapport bibliothèque", ln=True, align='C')
    pdf.ln(10)
    for livre in livres:
        pdf.cell(200, 10, txt=f"Livre: {livre.titre} - Auteur: {livre.auteur}", ln=True, align='L')
    pdf.ln(10)
    for membre in membres:
        pdf.cell(200, 10, txt=f"Membre: {membre.nom} {membre.prenom} - Email: {membre.email}", ln=True, align='L')
    pdf.ln(10)
    for emprunt in emprunts:
        pdf.cell(200, 10, txt=f"Emprunt: Livre {emprunt.livre_id} - Membre {emprunt.membre_id} - Date emprunt: {emprunt.date_emprunt} - Date retour: {emprunt.date_retour}", ln=True, align='L')
    pdf.output("rapport.pdf")
    return jsonify({'message': 'Rapport généré'})

if __name__ == "__main__":
    app.run(debug=True)
