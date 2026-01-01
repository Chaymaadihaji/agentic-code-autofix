# main.py

import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

# Initialisation des extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app)

# Modèle de patient
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)

# Modèle de rendez-vous
class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    heure = db.Column(db.Time, nullable=False)
    motif = db.Column(db.String(200), nullable=False)

# Modèle de médicament
class Medicament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    posologie = db.Column(db.String(200), nullable=False)
    debut_traitement = db.Column(db.DateTime, nullable=False)
    fin_traitement = db.Column(db.DateTime, nullable=False)

# Modèle de rapport
class Rapport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    contenu = db.Column(db.String(500), nullable=False)

# Modèle d'utilisateur
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# Schemas
class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nom', 'prenom', 'date_naissance', 'telephone', 'adresse')

class RendezVousSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'date', 'heure', 'motif')

class MedicamentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nom', 'posologie', 'debut_traitement', 'fin_traitement')

class RapportSchema(ma.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'date', 'contenu')

class UtilisateurSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email')

# Initialisation des schemas
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)
rendez_vous_schema = RendezVousSchema()
rendez_vous_schema = RendezVousSchema(many=True)
medicament_schema = MedicamentSchema()
medicaments_schema = MedicamentSchema(many=True)
rapport_schema = RapportSchema()
rapports_schema = RapportSchema(many=True)
utilisateur_schema = UtilisateurSchema()
utilisateurs_schema = UtilisateurSchema(many=True)

# Route pour les fiches patients
@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify(patients_schema.dump(patients))

# Route pour les rendez-vous
@app.route('/rendez-vous', methods=['GET'])
def get_rendez_vous():
    rendez_vous = RendezVous.query.all()
    return jsonify(rendez_vous_schema.dump(rendez_vous))

# Route pour les médicaments
@app.route('/medicaments', methods=['GET'])
def get_medicaments():
    medicaments = Medicament.query.all()
    return jsonify(medocaments_schema.dump(medicaments))

# Route pour les rapports
@app.route('/rapports', methods=['GET'])
def get_rapports():
    rapports = Rapport.query.all()
    return jsonify(rapports_schema.dump(rapports))

# Route pour les utilisateurs
@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return jsonify(utilisateurs_schema.dump(utilisateurs))

# Route pour la création d'un patient
@app.route('/patients', methods=['POST'])
def create_patient():
    patient = Patient(nom=request.json['nom'], prenom=request.json['prenom'], date_naissance=request.json['date_naissance'], telephone=request.json['telephone'], adresse=request.json['adresse'])
    db.session.add(patient)
    db.session.commit()
    return patient_schema.jsonify(patient)

# Route pour la création d'un rendez-vous
@app.route('/rendez-vous', methods=['POST'])
def create_rendez_vous():
    rendez_vous = RendezVous(patient_id=request.json['patient_id'], date=request.json['date'], heure=request.json['heure'], motif=request.json['motif'])
    db.session.add(rendez_vous)
    db.session.commit()
    return rendez_vous_schema.jsonify(rendez_vous)

# Route pour la création d'un médicament
@app.route('/medicaments', methods=['POST'])
def create_medicament():
    medicament = Medicament(nom=request.json['nom'], posologie=request.json['posologie'], debut_traitement=request.json['debut_traitement'], fin_traitement=request.json['fin_traitement'])
    db.session.add(medicament)
    db.session.commit()
    return medicament_schema.jsonify(medicament)

# Route pour la création d'un rapport
@app.route('/rapports', methods=['POST'])
def create_rapport():
    rapport = Rapport(patient_id=request.json['patient_id'], date=request.json['date'], contenu=request.json['contenu'])
    db.session.add(rapport)
    db.session.commit()
    return rapport_schema.jsonify(rapport)

# Route pour la création d'un utilisateur
@app.route('/utilisateurs', methods=['POST'])
def create_utilisateur():
    utilisateur = Utilisateur(username=request.json['username'], password=request.json['password'], email=request.json['email'])
    db.session.add(utilisateur)
    db.session.commit()
    return utilisateur_schema.jsonify(utilisateur)

# Route pour la connexion d'un utilisateur
@app.route('/login', methods=['POST'])
def login():
    utilisateur = Utilisateur.query.filter_by(username=request.json['username']).first()
    if utilisateur and bcrypt.check_password_hash(utilisateur.password, request.json['password']):
        return utilisateur_schema.jsonify(utilisateur)
    return jsonify({'erreur': 'Mauvais identifiant ou mot de passe'}), 401

# Route pour la création de rendez-vous
@app.route('/rendez-vous', methods=['PUT'])
def update_rendez_vous():
    rendez_vous = RendezVous.query.get(request.json['id'])
    rendez_vous.patient_id = request.json['patient_id']
    rendez_vous.date = request.json['date']
    rendez_vous.heure = request.json['heure']
    rendez_vous.motif = request.json['motif']
    db.session.commit()
    return rendez_vous_schema.jsonify(rendez_vous)

# Route pour la suppression d'un rendez-vous
@app.route('/rendez-vous', methods=['DELETE'])
def delete_rendez_vous():
    rendez_vous = RendezVous.query.get(request.json['id'])
    db.session.delete(rendez_vous)
    db.session.commit()
    return jsonify({'message': 'Rendez-vous supprimé avec succès'})

# Initialisation de l'application
@app.route('/')
def index():
    return render_template('index.html')

# Initialisation de l'application

# 🔧 ROUTE AJOUTÉE AUTOMATIQUEMENT (manquante dans le HTML)
@app.route('/envoi')
def envoi():
    import datetime
    return jsonify({
        "status": "success",
        "endpoint": "/envoi",
        "message": "Endpoint ajouté automatiquement",
        "timestamp": datetime.datetime.now().isoformat(),
        "data": {"sample": "Données de démonstration"}
    })


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
