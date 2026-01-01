import os
import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    medical_history = db.relationship('MedicalHistory', backref='patient', lazy=True)

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    symptoms = db.Column(db.String(100), nullable=False)
    diagnosis = db.Column(db.String(100), nullable=False)
    treatment = db.Column(db.String(100), nullable=False)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)

class MedicationAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    alert_date = db.Column(db.DateTime, nullable=False)

class SharedMedicalFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    file_content = db.Column(db.Text, nullable=False)

class HealthGraph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    graph_name = db.Column(db.String(100), nullable=False)
    graph_data = db.Column(db.Text, nullable=False)

class DoctorReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    report_name = db.Column(db.String(100), nullable=False)
    report_content = db.Column(db.Text, nullable=False)

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MedicalHistoryForm(FlaskForm):
    symptoms = StringField('Symptoms', validators=[DataRequired()])
    diagnosis = StringField('Diagnosis', validators=[DataRequired()])
    treatment = StringField('Treatment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PrescriptionForm(FlaskForm):
    medication = StringField('Medication', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    frequency = StringField('Frequency', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AppointmentForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MedicationAlertForm(FlaskForm):
    medication = StringField('Medication', validators=[DataRequired()])
    alert_date = StringField('Alert Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SharedMedicalFileForm(FlaskForm):
    file_name = StringField('File Name', validators=[DataRequired()])
    file_content = StringField('File Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class HealthGraphForm(FlaskForm):
    graph_name = StringField('Graph Name', validators=[DataRequired()])
    graph_data = StringField('Graph Data', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DoctorReportForm(FlaskForm):
    report_name = StringField('Report Name', validators=[DataRequired()])
    report_content = StringField('Report Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(name=form.name.data, date_of_birth=form.date_of_birth.data)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient.id))
    return render_template('index.html', form=form)

@app.route('/patient/<int:patient_id>', methods=['GET'])
def patient_detail(patient_id):
    patient = Patient.query.get(patient_id)
    medical_history = MedicalHistory.query.filter_by(patient_id=patient_id).all()
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    medication_alerts = MedicationAlert.query.filter_by(patient_id=patient_id).all()
    shared_medical_files = SharedMedicalFile.query.filter_by(patient_id=patient_id).all()
    health_graphs = HealthGraph.query.filter_by(patient_id=patient_id).all()
    doctor_reports = DoctorReport.query.filter_by(patient_id=patient_id).all()
    return render_template('patient_detail.html', patient=patient, medical_history=medical_history, prescriptions=prescriptions, appointments=appointments, medication_alerts=medication_alerts, shared_medical_files=shared_medical_files, health_graphs=health_graphs, doctor_reports=doctor_reports)

@app.route('/medical_history/<int:patient_id>', methods=['GET', 'POST'])
def medical_history(patient_id):
    form = MedicalHistoryForm()
    if form.validate_on_submit():
        medical_history = MedicalHistory(patient_id=patient_id, symptoms=form.symptoms.data, diagnosis=form.diagnosis.data, treatment=form.treatment.data)
        db.session.add(medical_history)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    return render_template('medical_history.html', form=form)

@app.route('/prescription/<int:patient_id>', methods=['GET', 'POST'])
def prescription(patient_id):
    form = PrescriptionForm()
    if form.validate_on_submit():
        prescription = Prescription(patient_id=patient_id, medication=form.medication.data, dosage=form.dosage.data, frequency=form.frequency.data)
        db.session.add(prescription)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    return render_template('prescription.html', form=form)

@app.route('/appointment/<int:patient_id>', methods=['GET', 'POST'])
def appointment(patient_id):
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(patient_id=patient_id, date=form.date.data, time=form.time.data)
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    return render_template('appointment.html', form=form)

@app.route('/medication_alert/<int:patient_id>', methods=['GET', 'POST'])
def medication_alert(patient_id):
    form = MedicationAlertForm()
    if form.validate_on_submit():
        medication_alert = MedicationAlert(patient_id=patient_id, medication=form.medication.data, alert_date=form.alert_date.data)
        db.session.add(medication_alert)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    return render_template('medication_alert.html', form=form)

@app.route('/shared_medical_file/<int:patient_id>', methods=['GET', 'POST'])
def shared_medical_file(patient_id):
    form = SharedMedicalFileForm()
    if form.validate_on_submit():
        shared_medical_file = SharedMedicalFile(patient_id=patient_id, file_name=form.file_name.data, file_content=form.file_content.data)
        db.session.add(shared_medical_file)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    return render_template('shared_medical_file.html', form=form)

@app.route('/health_graph/<int:patient_id>', methods=['GET', 'POST'])
def health_graph(patient_id):
    form = HealthGraphForm()
    if form.validate_on_submit():
        health_graph = HealthGraph(patient_id=patient_id, graph_name=form.graph_name.data, graph_data=form.graph_data.data)
        db.session.add(health_graph)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    return render_template('health_graph.html', form=form)

@app.route('/doctor_report/<int:patient_id>', methods=['GET', 'POST'])
def doctor_report(patient_id):
    form = DoctorReportForm()
    if form.validate_on_submit():
        doctor_report = DoctorReport(patient_id=patient_id, report_name=form.report_name.data, report_content=form.report_content.data)
        db.session.add(doctor_report)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    return render_template('doctor_report.html', form=form)

@app.route('/dashboard')
def dashboard():
    patients = Patient.query.all()
    return render_template('dashboard.html', patients=patients)

@app.route('/generate_graph/<int:patient_id>')
def generate_graph(patient_id):
    patient = Patient.query.get(patient_id)
    medical_history = MedicalHistory.query.filter_by(patient_id=patient_id).all()
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    appointments = Appointment.query.filter_by(patient_id=patient_id).all()
    medication_alerts = MedicationAlert.query.filter_by(patient_id=patient_id).all()
    shared_medical_files = SharedMedicalFile.query.filter_by(patient_id=patient_id).all()
    health_graphs = HealthGraph.query.filter_by(patient_id=patient_id).all()
    doctor_reports = DoctorReport.query.filter_by(patient_id=patient_id).all()
    df = pd.DataFrame({'Medical History': [history.symptoms for history in medical_history], 'Prescriptions': [prescription.medication for prescription in prescriptions], 'Appointments': [appointment.date for appointment in appointments], 'Medication Alerts': [alert.medication for alert in medication_alerts], 'Shared Medical Files': [file.file_name for file in shared_medical_files], 'Health Graphs': [graph.graph_name for graph in health_graphs], 'Doctor Reports': [report.report_name for report in doctor_reports]})
    plt.figure(figsize=(10,6))
    sns.set()
    sns.lineplot(data=df)
    plt.title('Patient Health Status')
    plt.xlabel('Time')
    plt.ylabel('Status')
    plt.savefig('static/graph.png')
    return jsonify({'message': 'Graph generated successfully'})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
