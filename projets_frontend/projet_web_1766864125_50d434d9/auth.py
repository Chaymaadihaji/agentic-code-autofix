# auth.py
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import pdfkit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['JWT_SECRET_KEY'] = 'secret-key'

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

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    nom = request.json['nom']
    prenom = request.json['prenom']
    password = request.json['password']
    membre = Membre.query.filter_by(nom=nom, prenom=prenom).first()
    if membre and membre.password == password:
        access_token = create_access_token(identity=membre.id)
        return jsonify(access_token=access_token)
    return jsonify(error='Membre non trouvé'), 401

@app.route('/livres', methods=['GET', 'POST'])
@jwt_required
def livres():
    if request.method == 'GET':
        return jsonify([{'id': l.id, 'titre': l.titre, 'auteur': l.auteur} for l in Livre.query.all()])
    elif request.method == 'POST':
        titre = request.json['titre']
        auteur = request.json['auteur']
        livre = Livre(titre=titre, auteur=auteur)
        db.session.add(livre)
        db.session.commit()
        return jsonify({'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur})

@app.route('/livres/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def livre(id):
    livre = Livre.query.get(id)
    if request.method == 'GET':
        return jsonify({'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur})
    elif request.method == 'PUT':
        titre = request.json['titre']
        auteur = request.json['auteur']
        livre.titre = titre
        livre.auteur = auteur
        db.session.commit()
        return jsonify({'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur})
    elif request.method == 'DELETE':
        db.session.delete(livre)
        db.session.commit()
        return jsonify({'message': 'Livre supprimé'})

@app.route('/membres', methods=['GET', 'POST'])
@jwt_required
def membres():
    if request.method == 'GET':
        return jsonify([{'id': m.id, 'nom': m.nom, 'prenom': m.prenom} for m in Membre.query.all()])
    elif request.method == 'POST':
        nom = request.json['nom']
        prenom = request.json['prenom']
        membre = Membre(nom=nom, prenom=prenom)
        db.session.add(membre)
        db.session.commit()
        return jsonify({'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom})

@app.route('/membres/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def membre(id):
    membre = Membre.query.get(id)
    if request.method == 'GET':
        return jsonify({'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom})
    elif request.method == 'PUT':
        nom = request.json['nom']
        prenom = request.json['prenom']
        membre.nom = nom
        membre.prenom = prenom
        db.session.commit()
        return jsonify({'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom})
    elif request.method == 'DELETE':
        db.session.delete(membre)
        db.session.commit()
        return jsonify({'message': 'Membre supprimé'})

@app.route('/emprunts', methods=['GET', 'POST'])
@jwt_required
def emprunts():
    if request.method == 'GET':
        return jsonify([{'id': e.id, 'livre_id': e.livre_id, 'membre_id': e.membre_id} for e in Emprunt.query.all()])
    elif request.method == 'POST':
        livre_id = request.json['livre_id']
        membre_id = request.json['membre_id']
        emprunt = Emprunt(livre_id=livre_id, membre_id=membre_id)
        db.session.add(emprunt)
        db.session.commit()
        return jsonify({'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id})

@app.route('/emprunts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def emprunt(id):
    emprunt = Emprunt.query.get(id)
    if request.method == 'GET':
        return jsonify({'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id})
    elif request.method == 'PUT':
        livre_id = request.json['livre_id']
        membre_id = request.json['membre_id']
        emprunt.livre_id = livre_id
        emprunt.membre_id = membre_id
        db.session.commit()
        return jsonify({'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id})
    elif request.method == 'DELETE':
        db.session.delete(emprunt)
        db.session.commit()
        return jsonify({'message': 'Emprunt supprimé'})

@app.route('/rapport', methods=['GET'])
@jwt_required
def rapport():
    livres = Livre.query.all()
    membres = Membre.query.all()
    emprunts = Emprunt.query.all()
    pdfkit.from_url('http://localhost:5000/emprunts', 'rapport.pdf')
    return jsonify({'message': 'Rapport généré'})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
