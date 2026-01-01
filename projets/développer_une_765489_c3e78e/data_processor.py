# data_processor.py

import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Fiches patients détaillées
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.DateTime, nullable=False)

# Historique médical
class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)

# Ordonnances numériques
class Ordonnance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    medicament = db.Column(db.String(100), nullable=False)
    dose = db.Column(db.String(100), nullable=False)

# Prise de rendez-vous
class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    heure = db.Column(db.Time, nullable=False)

# Alertes médicaments
class Alerte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)

# Dossier médical partagé
class Dossier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    fichier = db.Column(db.LargeBinary, nullable=False)

# Graphiques de suivi santé
def graphiques_patient(patient_id):
    patient = Patient.query.get(patient_id)
    historiques = Historique.query.filter_by(patient_id=patient_id).all()
    ordonnances = Ordonnance.query.filter_by(patient_id=patient_id).all()
    rendez_vous = RendezVous.query.filter_by(patient_id=patient_id).all()
    alertes = Alerte.query.filter_by(patient_id=patient_id).all()

    plt.figure(figsize=(10, 6))
    sns.set_style('whitegrid')
    sns.lineplot(x=[h.date for h in historiques], y=[h.description for h in historiques])
    plt.title('Historique médical')
    plt.xlabel('Date')
    plt.ylabel('Description')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.set_style('whitegrid')
    sns.scatterplot(x=[o.date for o in ordonnances], y=[o.dose for o in ordonnances])
    plt.title('Ordonnances numériques')
    plt.xlabel('Date')
    plt.ylabel('Dose')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.set_style('whitegrid')
    sns.barplot(x=[r.date for r in rendez_vous], y=[r.heure for r in rendez_vous])
    plt.title('Rendez-vous')
    plt.xlabel('Date')
    plt.ylabel('Heure')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.set_style('whitegrid')
    sns.barplot(x=[a.date for a in alertes], y=[a.description for a in alertes])
    plt.title('Alertes médicaments')
    plt.xlabel('Date')
    plt.ylabel('Description')
    plt.show()

# Rapports pour médecins
def rapport_medicin(patient_id):
    patient = Patient.query.get(patient_id)
    historiques = Historique.query.filter_by(patient_id=patient_id).all()
    ordonnances = Ordonnance.query.filter_by(patient_id=patient_id).all()
    rendez_vous = RendezVous.query.filter_by(patient_id=patient_id).all()
    alertes = Alerte.query.filter_by(patient_id=patient_id).all()

    rapport = {
        'patient': patient.nom + ' ' + patient.prenom,
        'historique': [h.description for h in historiques],
        'ordonnances': [o.medicament for o in ordonnances],
        'rendez-vous': [r.heure for r in rendez_vous],
        'alertes': [a.description for a in alertes]
    }

    return rapport

# Chiffrement des données
def chiffrement_donnees(data):
    return generate_password_hash(data)

# API pour les données en temps réel
@app.route('/donnees', methods=['GET'])
def donnees():
    patient_id = request.args.get('patient_id')
    data = Patient.query.get(patient_id)
    return jsonify({'data': data})

# Structure modulaire pour différentes visualisations
@app.route('/graphiques', methods=['GET'])
def graphiques():
    patient_id = request.args.get('patient_id')
    graphiques_patient(patient_id)
    return jsonify({'message': 'Graphiques générés'})

# Route pour la création d'un patient
@app.route('/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    patient = Patient(nom=data['nom'], prenom=data['prenom'], date_naissance=data['date_naissance'])
    db.session.add(patient)
    db.session.commit()
    return jsonify({'message': 'Patient créé'})

# Route pour la création d'un rendez-vous
@app.route('/rendez-vous', methods=['POST'])
def create_rendez_vous():
    data = request.get_json()
    rendez_vous = RendezVous(patient_id=data['patient_id'], date=data['date'], heure=data['heure'])
    db.session.add(rendez_vous)
    db.session.commit()
    return jsonify({'message': 'Rendez-vous créé'})

# Route pour la création d'une ordonnance
@app.route('/ordonnances', methods=['POST'])
def create_ordonnance():
    data = request.get_json()
    ordonnance = Ordonnance(patient_id=data['patient_id'], date=data['date'], medicament=data['medicament'], dose=data['dose'])
    db.session.add(ordonnance)
    db.session.commit()
    return jsonify({'message': 'Ordonnance créée'})

# Route pour la création d'une alerte
@app.route('/alertes', methods=['POST'])
def create_alerte():
    data = request.get_json()
    alerte = Alerte(patient_id=data['patient_id'], date=data['date'], description=data['description'])
    db.session.add(alerte)
    db.session.commit()
    return jsonify({'message': 'Alerte créée'})

# Route pour la création d'un dossier médical
@app.route('/dossiers', methods=['POST'])
def create_dossier():
    data = request.get_json()
    dossier = Dossier(patient_id=data['patient_id'], fichier=data['fichier'])
    db.session.add(dossier)
    db.session.commit()
    return jsonify({'message': 'Dossier médical créé'})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
