# dashboard.py

import os
import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configuration de l'application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(32)

# Initialisation des outils
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
limiter = Limiter(app, key_func=get_remote_address)

# Modèles de données
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)

class Ordonnance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medicament = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)

class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    heure = db.Column(db.Time, nullable=False)

class DossierMedical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)

# Fonctionnalités
@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/fiches_patients')
def fiches_patients():
    patients = Patient.query.all()
    return render_template('fiches_patients.html', patients=patients)

@app.route('/historique_medical')
def historique_medical():
    patients = Patient.query.all()
    return render_template('historique_medical.html', patients=patients)

@app.route('/ordonnances')
def ordonnances():
    ordonnances = Ordonnance.query.all()
    return render_template('ordonnances.html', ordonnances=ordonnances)

@app.route('/rendez_vous')
def rendez_vous():
    rendez_vous = RendezVous.query.all()
    return render_template('rendez_vous.html', rendez_vous=rendez_vous)

@app.route('/dossier_medical')
def dossier_medical():
    dossiers_medicaux = DossierMedical.query.all()
    return render_template('dossier_medical.html', dossiers_medicaux=dossiers_medicaux)

@app.route('/graphiques')
def graphiques():
    patients = Patient.query.all()
    return render_template('graphiques.html', patients=patients)

@app.route('/rapports')
def rapports():
    patients = Patient.query.all()
    return render_template('rapports.html', patients=patients)

@app.route('/chiffrement')
def chiffrement():
    patient = Patient.query.first()
    password = request.form['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    patient.password = hashed_password
    db.session.commit()
    return 'Chiffrement effectué'

if __name__ == '__main__':
    app.run(debug=True)
