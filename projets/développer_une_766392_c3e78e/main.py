# main.py

import os
import json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    date_naissance = db.Column(db.DateTime, nullable=False)
    numero_telephone = db.Column(db.String(20), nullable=False)
    dossier_medical = db.relationship('DossierMedical', backref='patient', lazy=True)

class DossierMedical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    historique_medicale = db.Column(db.Text, nullable=False)
    ordonnance_numerique = db.Column(db.Text, nullable=False)
    prise_rendez_vous = db.Column(db.DateTime, nullable=False)

class Medecin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    numero_telephone = db.Column(db.String(20), nullable=False)
    dossier_medical = db.relationship('DossierMedical', backref='medecin', lazy=True)

class Medicament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    dose = db.Column(db.Float, nullable=False)
    dosage = db.Column(db.Float, nullable=False)

class AlerteMedicament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicament_id = db.Column(db.Integer, db.ForeignKey('medicament.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date_alerte = db.Column(db.DateTime, nullable=False)

class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecin.id'), nullable=False)
    date_rendez_vous = db.Column(db.DateTime, nullable=False)

class Rapport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecin.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date_rapport = db.Column(db.DateTime, nullable=False)

# Génération de données pour le dashboard
patients = []
for i in range(10):
    patient = Patient(nom=f"Patient {i}", prenom=f"Prenom {i}", date_naissance=datetime(1990, 1, 1), numero_telephone=f"06{i}")
    patients.append(patient)
db.session.add_all(patients)
db.session.commit()

medicaments = []
for i in range(10):
    medicament = Medicament(nom=f"Medicament {i}", description=f"Description {i}", dose=float(i), dosage=float(i))
    medicaments.append(medicament)
db.session.add_all(medicaments)
db.session.commit()

alerts = []
for i in range(10):
    alerte = AlerteMedicament(medicament_id=i, patient_id=i, date_alerte=datetime(2022, 1, 1))
    alerts.append(alerte)
db.session.add_all(alerts)
db.session.commit()

rendez_vous = []
for i in range(10):
    rendez = RendezVous(patient_id=i, medecin_id=i, date_rendez_vous=datetime(2022, 1, 1))
    rendez_vous.append(rendez)
db.session.add_all(rendez_vous)
db.session.commit()

rapports = []
for i in range(10):
    rapport = Rapport(medecin_id=i, patient_id=i, date_rapport=datetime(2022, 1, 1))
    rapports.append(rapport)
db.session.add_all(rapports)
db.session.commit()

# Calcul des statistiques/métriques
statistiques = []
for patient in patients:
    statistiques.append({'patient': patient.nom, 'medicaments': len(db.session.query(AlerteMedicament).filter_by(patient_id=patient.id).all())})

# API pour les données en temps réel
@app.route('/api/data', methods=['GET'])
def get_data():
    return json.dumps({'patients': [patient.__dict__ for patient in patients], 'medicaments': [medicament.__dict__ for medicament in medicaments]})

# Structure modulaire pour différentes visualisations
@app.route('/')
def index():
    return render_template('index.html', patients=patients, medicaments=medicaments, statistiques=statistiques)

if __name__ == "__main__":
    app.run(debug=True)
