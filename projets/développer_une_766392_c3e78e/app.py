# app.py

import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(100), nullable=False)

class Ordonnance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medicament = db.Column(db.String(100), nullable=False)
    dose = db.Column(db.String(100), nullable=False)

class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    heure = db.Column(db.String(100), nullable=False)

class DossierMedical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
@jwt_required
def patients():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@app.route('/patients/<int:id>')
@jwt_required
def patient(id):
    patient = Patient.query.get(id)
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({'error': 'Patient not found'}), 404

@app.route('/ordonnances')
@jwt_required
def ordonnances():
    ordonnances = Ordonnance.query.all()
    return jsonify([ordonnance.to_dict() for ordonnance in ordonnances])

@app.route('/rendez-vous')
@jwt_required
def rendezVous():
    rendezVous = RendezVous.query.all()
    return jsonify([rendezVous.to_dict() for rendezVous in rendezVous])

@app.route('/dossier-medical')
@jwt_required
def dossierMedical():
    dossierMedical = DossierMedical.query.all()
    return jsonify([dossierMedical.to_dict() for dossierMedical in dossierMedical])

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    mot_de_passe = request.json['mot_de_passe']
    patient = Patient.query.filter_by(email=email).first()
    if patient and bcrypt.check_password_hash(patient.mot_de_passe, mot_de_passe):
        access_token = create_access_token(identity=patient.id)
        return jsonify({'access_token': access_token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    mot_de_passe = bcrypt.generate_password_hash(request.json['mot_de_passe']).decode('utf-8')
    patient = Patient(nom=nom, prenom=prenom, email=email, mot_de_passe=mot_de_passe)
    db.session.add(patient)
    db.session.commit()
    return jsonify({'message': 'Patient created successfully'})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
