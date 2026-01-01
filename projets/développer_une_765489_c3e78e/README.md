# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)

class Ordonnance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicament = db.Column(db.String(100), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    patients = Patient.query.all()
    ordonnances = Ordonnance.query.all()
    return render_template('index.html', patients=patients, ordonnances=ordonnances)

@app.route('/patients')
def liste_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@app.route('/ordonnances')
def liste_ordonnances():
    ordonnances = Ordonnance.query.all()
    return render_template('ordonnances.html', ordonnances=ordonnances)

@app.route('/ajouter_patient', methods=['GET', 'POST'])
def ajouter_patient():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        patient = Patient(nom=nom, prenom=prenom)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('liste_patients'))
    return render_template('ajouter_patient.html')

@app.route('/ajouter_ordonnance', methods=['GET', 'POST'])
def ajouter_ordonnance():
    if request.method == 'POST':
        medicament = request.form['medicament']
        quantite = request.form['quantite']
        ordonnance = Ordonnance(medicament=medicament, quantite=quantite)
        db.session.add(ordonnance)
        db.session.commit()
        return redirect(url_for('liste_ordonnances'))
    return render_template('ajouter_ordonnance.html')

if __name__ == '__main__':
    app.run(debug=True)
