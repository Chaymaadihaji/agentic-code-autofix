from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

class Medicament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medicament_id = db.Column(db.Integer, db.ForeignKey('medicament.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/patient/<int:patient_id>')
def patient(patient_id):
    patient = Patient.query.get(patient_id)
    medical_history = MedicalHistory.query.filter_by(patient_id=patient_id).all()
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    alerts = Alert.query.filter_by(patient_id=patient_id).all()
    return render_template('patient.html', patient=patient, medical_history=medical_history, prescriptions=prescriptions, appointments=appointments, alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True)
