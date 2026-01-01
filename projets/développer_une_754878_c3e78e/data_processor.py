# data_processor.py

import json
import os
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    historique_medical = db.relationship('HistoriqueMedical', backref='patient', lazy=True)

class HistoriqueMedical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    ordonnance_numerique = db.Column(db.String(100), nullable=False)

class OrdonnanceNumerique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    medicament = db.Column(db.String(100), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    heure = db.Column(db.Time, nullable=False)

class Medecin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)

class DossierMedicalPartage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecin.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

class GraphiqueSuiviSante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    valeur = db.Column(db.Float, nullable=False)

class RapportPourMedecin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecin.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/patient/<int:patient_id>')
def patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        return render_template('patient.html', patient=patient)
    return jsonify({'error': 'Patient not found'})

@app.route('/ordonnance/<int:patient_id>')
def ordonnance(patient_id):
    ordonnances = OrdonnanceNumerique.query.filter_by(patient_id=patient_id).all()
    return jsonify([o.to_dict() for o in ordonnances])

@app.route('/rendez-vous/<int:patient_id>')
def rendez_vous(patient_id):
    rendez_vous = RendezVous.query.filter_by(patient_id=patient_id).all()
    return jsonify([rv.to_dict() for rv in rendez_vous])

@app.route('/medecin/<int:medecin_id>')
def medecin(medecin_id):
    medecin = Medecin.query.get(medecin_id)
    if medecin:
        return render_template('medecin.html', medecin=medecin)
    return jsonify({'error': 'Médecin not found'})

@app.route('/dossier-medical/<int:patient_id>')
def dossier_medical(patient_id):
    dossier_medical = DossierMedicalPartage.query.filter_by(patient_id=patient_id).all()
    return jsonify([dm.to_dict() for dm in dossier_medical])

@app.route('/graphique/<int:patient_id>')
def graphique(patient_id):
    graphique = GraphiqueSuiviSante.query.filter_by(patient_id=patient_id).all()
    return jsonify([g.to_dict() for g in graphique])

@app.route('/rapport/<int:patient_id>')
def rapport(patient_id):
    rapport = RapportPourMedecin.query.filter_by(patient_id=patient_id).all()
    return jsonify([r.to_dict() for r in rapport])

if __name__ == "__main__":
    db.create_all()
    with open('data.json', 'w') as f:
        json.dump({
            'patients': [
                {'id': 1, 'nom': 'Dupont', 'prenom': 'Jean', 'date_naissance': '1990-01-01', 'adresse': 'Rue de la République', 'telephone': '0123456789'},
                {'id': 2, 'nom': 'Martin', 'prenom': 'Pierre', 'date_naissance': '1995-02-02', 'adresse': 'Rue de la Liberté', 'telephone': '0987654321'}
            ],
            'historique_medical': [
                {'id': 1, 'patient_id': 1, 'date': '2022-01-01', 'description': 'Consultation initiale', 'ordonnance_numerique': '10mg'},
                {'id': 2, 'patient_id': 1, 'date': '2022-02-02', 'description': 'Consultation de suivi', 'ordonnance_numerique': '20mg'}
            ],
            'ordonnance_numerique': [
                {'id': 1, 'patient_id': 1, 'date': '2022-01-01', 'medicament': 'Paracetamol', 'quantite': 10},
                {'id': 2, 'patient_id': 1, 'date': '2022-02-02', 'medicament': 'Ibuprofène', 'quantite': 20}
            ],
            'rendez-vous': [
                {'id': 1, 'patient_id': 1, 'date': '2022-01-01', 'heure': '10:00'},
                {'id': 2, 'patient_id': 1, 'date': '2022-02-02', 'heure': '14:00'}
            ],
            'medecin': [
                {'id': 1, 'nom': 'Smith', 'prenom': 'John', 'telephone': '0123456789'},
                {'id': 2, 'nom': 'Johnson', 'prenom': 'Jane', 'telephone': '0987654321'}
            ],
            'dossier_medical': [
                {'id': 1, 'patient_id': 1, 'medecin_id': 1, 'date': '2022-01-01'},
                {'id': 2, 'patient_id': 1, 'medecin_id': 2, 'date': '2022-02-02'}
            ],
            'graphique': [
                {'id': 1, 'patient_id': 1, 'date': '2022-01-01', 'valeur': 10.5},
                {'id': 2, 'patient_id': 1, 'date': '2022-02-02', 'valeur': 20.8}
            ],
            'rapport': [
                {'id': 1, 'patient_id': 1, 'medecin_id': 1, 'date': '2022-01-01'},
                {'id': 2, 'patient_id': 1, 'medecin_id': 2, 'date': '2022-02-02'}
            ]
        }, f)
    app.run(debug=True)

class Patient:
    def to_dict(self):
        return {'id': self.id, 'nom': self.nom, 'prenom': self.prenom, 'date_naissance': self.date_naissance, 'adresse': self.adresse, 'telephone': self.telephone}

class HistoriqueMedical:
    def to_dict(self):
        return {'id': self.id, 'patient_id': self.patient_id, 'date': self.date, 'description': self.description, 'ordonnance_numerique': self.ordonnance_numerique}

class OrdonnanceNumerique:
    def to_dict(self):
        return {'id': self.id, 'patient_id': self.patient_id, 'date': self.date, 'medicament': self.medicament, 'quantite': self.quantite}

class RendezVous:
    def to_dict(self):
        return {'id': self.id, 'patient_id': self.patient_id, 'date': self.date, 'heure': self.heure}

class Medecin:
    def to_dict(self):
        return {'id': self.id, 'nom': self.nom, 'prenom': self.prenom, 'telephone': self.telephone}

class DossierMedicalPartage:
    def to_dict(self):
        return {'id': self.id, 'patient_id': self.patient_id, 'medecin_id': self.medecin_id, 'date': self.date}

class GraphiqueSuiviSante:
    def to_dict(self):
        return {'id': self.id, 'patient_id': self.patient_id, 'date': self.date, 'valeur': self.valeur}

class RapportPourMedecin:
    def to_dict(self):
        return {'id': self.id, 'patient_id': self.patient_id, 'medecin_id': self.medecin_id, 'date': self.date}
