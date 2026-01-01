# database.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['JWT_SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    edition = db.Column(db.Integer, nullable=False)

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
    date_retour = db.Column(db.DateTime, nullable=True)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    membre = Membre.query.filter_by(email=email).first()
    if membre and membre.password == password:
        access_token = create_access_token(identity=membre.id)
        return jsonify(access_token=access_token)
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/livres', methods=['GET', 'POST'])
@jwt_required
def livres():
    if request.method == 'GET':
        return jsonify([l.to_dict() for l in Livre.query.all()])
    titre = request.json.get('titre')
    auteur = request.json.get('auteur')
    edition = request.json.get('edition')
    livre = Livre(titre=titre, auteur=auteur, edition=edition)
    db.session.add(livre)
    db.session.commit()
    return jsonify(livre.to_dict())

@app.route('/livres/<int:id>', methods=['GET', 'DELETE'])
@jwt_required
def livre(id):
    livre = Livre.query.get(id)
    if request.method == 'GET':
        return jsonify(livre.to_dict())
    db.session.delete(livre)
    db.session.commit()
    return jsonify({'message': 'Livre supprimé'})

@app.route('/membres', methods=['GET', 'POST'])
@jwt_required
def membres():
    if request.method == 'GET':
        return jsonify([m.to_dict() for m in Membre.query.all()])
    nom = request.json.get('nom')
    prenom = request.json.get('prenom')
    email = request.json.get('email')
    password = request.json.get('password')
    membre = Membre(nom=nom, prenom=prenom, email=email, password=password)
    db.session.add(membre)
    db.session.commit()
    return jsonify(membre.to_dict())

@app.route('/membres/<int:id>', methods=['GET', 'DELETE'])
@jwt_required
def membre(id):
    membre = Membre.query.get(id)
    if request.method == 'GET':
        return jsonify(membre.to_dict())
    db.session.delete(membre)
    db.session.commit()
    return jsonify({'message': 'Membre supprimé'})

@app.route('/emprunts', methods=['GET', 'POST'])
@jwt_required
def emprunts():
    if request.method == 'GET':
        return jsonify([e.to_dict() for e in Emprunt.query.all()])
    livre_id = request.json.get('livre_id')
    membre_id = request.json.get('membre_id')
    date_emprunt = request.json.get('date_emprunt')
    emprunt = Emprunt(livre_id=livre_id, membre_id=membre_id, date_emprunt=date_emprunt)
    db.session.add(emprunt)
    db.session.commit()
    return jsonify(emprunt.to_dict())

@app.route('/emprunts/<int:id>', methods=['GET', 'DELETE'])
@jwt_required
def emprunt(id):
    emprunt = Emprunt.query.get(id)
    if request.method == 'GET':
        return jsonify(emprunt.to_dict())
    db.session.delete(emprunt)
    db.session.commit()
    return jsonify({'message': 'Emprunt supprimé'})

@app.route('/stats', methods=['GET'])
@jwt_required
def stats():
    livres = Livre.query.count()
    membres = Membre.query.count()
    emprunts = Emprunt.query.count()
    return jsonify({'livres': livres, 'membres': membres, 'emprunts': emprunts})

if __name__ == "__main__":
    app.run(debug=True)
