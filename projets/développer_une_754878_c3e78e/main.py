# main.py

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from werkzeug.security import generate_password_hash
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.DateTime, nullable=False)
    ordonnances = db.relationship('Ordonnance', backref='patient', lazy=True)

class Ordonnance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medicament = db.Column(db.String(100), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class RDV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    heure = db.Column(db.String(100), nullable=False)

class Medicament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

class DossierMedicale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    contenu = db.Column(db.String(1000), nullable=False)

@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/ajouter_patient', methods=['GET', 'POST'])
def ajouter_patient():
    if request.method == 'POST':
        patient = Patient(nom=request.form['nom'], prenom=request.form['prenom'], date_naissance=request.form['date_naissance'])
        db.session.add(patient)
        db.session.commit()
    return render_template('ajouter_patient.html')

@app.route('/ordonnances', methods=['GET', 'POST'])
def ordonnances():
    if request.method == 'POST':
        ordonnance = Ordonnance(patient_id=request.form['patient_id'], medicament=request.form['medicament'], quantite=request.form['quantite'])
        db.session.add(ordonnance)
        db.session.commit()
    patients = Patient.query.all()
    ordonnances = Ordonnance.query.all()
    return render_template('ordonnances.html', patients=patients, ordonnances=ordonnances)

@app.route('/rdvs', methods=['GET', 'POST'])
def rdvs():
    if request.method == 'POST':
        rdv = RDV(patient_id=request.form['patient_id'], date=request.form['date'], heure=request.form['heure'])
        db.session.add(rdv)
        db.session.commit()
    patients = Patient.query.all()
    rdvs = RDV.query.all()
    return render_template('rdvs.html', patients=patients, rdvs=rdvs)

@app.route('/medicaments', methods=['GET', 'POST'])
def medicaments():
    if request.method == 'POST':
        medicament = Medicament(nom=request.form['nom'], description=request.form['description'])
        db.session.add(medicament)
        db.session.commit()
    medicaments = Medicament.query.all()
    return render_template('medicaments.html', medicaments=medicaments)

@app.route('/dossier_medicale', methods=['GET', 'POST'])
def dossier_medicale():
    if request.method == 'POST':
        dossier = DossierMedicale(patient_id=request.form['patient_id'], contenu=request.form['contenu'])
        db.session.add(dossier)
        db.session.commit()
    patients = Patient.query.all()
    dossiers = DossierMedicale.query.all()
    return render_template('dossier_medicale.html', patients=patients, dossiers=dossiers)

@app.route('/graphiques', methods=['GET', 'POST'])
def graphiques():
    patients = Patient.query.all()
    ordonnances = Ordonnance.query.all()
    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    for patient in patients:
        patient_id = patient.id
        for ordonnance in ordonnances:
            if ordonnance.patient_id == patient_id:
                x.append(patient_id)
                y.append(ordonnance.quantite)
    ax.plot(x, y)
    canvas = FigureCanvas(fig)
    return render_template('graphiques.html', x=x, y=y, fig=fig)

@app.route('/rapports', methods=['GET', 'POST'])
def rapports():
    patients = Patient.query.all()
    ordonnances = Ordonnance.query.all()
    rapport = ""
    for patient in patients:
        patient_id = patient.id
        for ordonnance in ordonnances:
            if ordonnance.patient_id == patient_id:
                rapport += f"Patient {patient_id} : {ordonnance.medicament} ({ordonnance.quantite})\n"
    return render_template('rapports.html', rapport=rapport)

if __name__ == "__main__":
    app.run(debug=True)
