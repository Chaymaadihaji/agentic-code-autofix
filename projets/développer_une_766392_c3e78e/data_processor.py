import json
from flask import Flask, render_template, request
from bokeh.plotting import figure, show
import pandas as pd
from datetime import datetime
from random import randint, choice

app = Flask(__name__)

# JSON data
data = {
    "patients": [
        {"id": 1, "name": "John Doe", "age": 30},
        {"id": 2, "name": "Jane Doe", "age": 25},
        {"id": 3, "name": "Bob Smith", "age": 40}
    ],
    "medical_history": [
        {"id": 1, "patient_id": 1, "date": "2022-01-01", "description": "Vaccination"},
        {"id": 2, "patient_id": 1, "date": "2022-02-01", "description": "Consultation"},
        {"id": 3, "patient_id": 2, "date": "2022-03-01", "description": "Analyse de sang"}
    ],
    "prescriptions": [
        {"id": 1, "patient_id": 1, "medicine": "Aspirine", "quantity": 10},
        {"id": 2, "patient_id": 1, "medicine": "Ibuprofène", "quantity": 20},
        {"id": 3, "patient_id": 2, "medicine": "Acétaminophène", "quantity": 15}
    ],
    "appointments": [
        {"id": 1, "patient_id": 1, "date": "2022-04-01", "heure": "10:00"},
        {"id": 2, "patient_id": 2, "date": "2022-05-01", "heure": "14:00"},
        {"id": 3, "patient_id": 3, "date": "2022-06-01", "heure": "09:00"}
    ],
    "alerts": [
        {"id": 1, "patient_id": 1, "medicine": "Aspirine", "expiration_date": "2022-07-01"},
        {"id": 2, "patient_id": 1, "medicine": "Ibuprofène", "expiration_date": "2022-08-01"},
        {"id": 3, "patient_id": 2, "medicine": "Acétaminophène", "expiration_date": "2022-09-01"}
    ],
    "shared_folder": [
        {"id": 1, "patient_id": 1, "file_name": "Dossier médical", "date": "2022-01-01"},
        {"id": 2, "patient_id": 1, "file_name": "Rapports médicaux", "date": "2022-02-01"},
        {"id": 3, "patient_id": 2, "file_name": "Dossiers de santé", "date": "2022-03-01"}
    ],
    "health_progress": [
        {"id": 1, "patient_id": 1, "date": "2022-04-01", "value": 10},
        {"id": 2, "patient_id": 1, "date": "2022-05-01", "value": 20},
        {"id": 3, "patient_id": 2, "date": "2022-06-01", "value": 15}
    ],
    "medical_reports": [
        {"id": 1, "patient_id": 1, "date": "2022-07-01", "description": "Rapport médical"},
        {"id": 2, "patient_id": 1, "date": "2022-08-01", "description": "Analyse de santé"},
        {"id": 3, "patient_id": 2, "date": "2022-09-01", "description": "Conseils médicaux"}
    ]
}

# Calcul des statistiques/métriques
def stats(patients):
    ages = [patient["age"] for patient in patients]
    avg_age = sum(ages) / len(ages)
    return avg_age

# API pour les données en temps réel
@app.route("/api/data", methods=["GET"])
def get_data():
    return json.dumps(data)

# Route pour la page d'accueil
@app.route("/")
def index():
    patients = data["patients"]
    avg_age = stats(patients)
    return render_template("index.html", patients=patients, avg_age=avg_age)

# Route pour les fiches patients détaillées
@app.route("/patient/<int:patient_id>")
def patient_detail(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        # Calcul des statistiques pour le patient
        medical_history = [mh for mh in data["medical_history"] if mh["patient_id"] == patient_id]
        prescriptions = [p for p in data["prescriptions"] if p["patient_id"] == patient_id]
        appointments = [a for a in data["appointments"] if a["patient_id"] == patient_id]
        alerts = [a for a in data["alerts"] if a["patient_id"] == patient_id]
        shared_folder = [sf for sf in data["shared_folder"] if sf["patient_id"] == patient_id]
        health_progress = [hp for hp in data["health_progress"] if hp["patient_id"] == patient_id]
        medical_reports = [mr for mr in data["medical_reports"] if mr["patient_id"] == patient_id]
        return render_template("patient_detail.html", patient=patient, medical_history=medical_history, prescriptions=prescriptions, appointments=appointments, alerts=alerts, shared_folder=shared_folder, health_progress=health_progress, medical_reports=medical_reports)
    return "Patient not found", 404

# Route pour les historiques médicaux
@app.route("/medical_history/<int:patient_id>")
def medical_history(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        medical_history = [mh for mh in data["medical_history"] if mh["patient_id"] == patient_id]
        return render_template("medical_history.html", patient=patient, medical_history=medical_history)
    return "Patient not found", 404

# Route pour les ordonnances numériques
@app.route("/prescriptions/<int:patient_id>")
def prescriptions(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        prescriptions = [p for p in data["prescriptions"] if p["patient_id"] == patient_id]
        return render_template("prescriptions.html", patient=patient, prescriptions=prescriptions)
    return "Patient not found", 404

# Route pour les rendez-vous
@app.route("/appointments/<int:patient_id>")
def appointments(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        appointments = [a for a in data["appointments"] if a["patient_id"] == patient_id]
        return render_template("appointments.html", patient=patient, appointments=appointments)
    return "Patient not found", 404

# Route pour les alertes médicaments
@app.route("/alerts/<int:patient_id>")
def alerts(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        alerts = [a for a in data["alerts"] if a["patient_id"] == patient_id]
        return render_template("alerts.html", patient=patient, alerts=alerts)
    return "Patient not found", 404

# Route pour le dossier médical partagé
@app.route("/shared_folder/<int:patient_id>")
def shared_folder(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        shared_folder = [sf for sf in data["shared_folder"] if sf["patient_id"] == patient_id]
        return render_template("shared_folder.html", patient=patient, shared_folder=shared_folder)
    return "Patient not found", 404

# Route pour les graphiques de suivi santé
@app.route("/health_progress/<int:patient_id>")
def health_progress(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        health_progress = [hp for hp in data["health_progress"] if hp["patient_id"] == patient_id]
        # Génération du graphique
        p = figure(title="Suivi santé", x_axis_label="Date", y_axis_label="Valeur")
        p.line([hp["date"] for hp in health_progress], [hp["value"] for hp in health_progress])
        return render_template("health_progress.html", patient=patient, health_progress=health_progress, p=p)
    return "Patient not found", 404

# Route pour les rapports pour médecins
@app.route("/medical_reports/<int:patient_id>")
def medical_reports(patient_id):
    patient = next((p for p in data["patients"] if p["id"] == patient_id), None)
    if patient:
        medical_reports = [mr for mr in data["medical_reports"] if mr["patient_id"] == patient_id]
        return render_template("medical_reports.html", patient=patient, medical_reports=medical_reports)
    return "Patient not found", 404

if __name__ == "__main__":
    app.run(debug=True)
