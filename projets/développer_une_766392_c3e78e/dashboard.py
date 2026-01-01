# dashboard.py

import json
from flask import Flask, render_template, request
from datetime import datetime
import statistics
import random

app = Flask(__name__)

# Fiches patients détaillées
patients = [
    {"id": 1, "nom": "Patient 1", "prenom": "Jean", "date_naissance": "1990-01-01"},
    {"id": 2, "nom": "Patient 2", "prenom": "Pierre", "date_naissance": "1995-06-01"},
    {"id": 3, "nom": "Patient 3", "prenom": "Marc", "date_naissance": "1980-03-01"}
]

# Historique médical
historique = [
    {"id": 1, "patient_id": 1, "date": "2022-01-01", "description": "Consultation"},
    {"id": 2, "patient_id": 1, "date": "2022-01-15", "description": "Analyse de sang"},
    {"id": 3, "patient_id": 2, "date": "2022-02-01", "description": "Consultation"}
]

# Ordonnances numériques
ordonnances = [
    {"id": 1, "patient_id": 1, "medicament": "Ibuprofène", "dosage": 2},
    {"id": 2, "patient_id": 1, "medicament": "Acetaminophène", "dosage": 3},
    {"id": 3, "patient_id": 2, "medicament": "Paracetamol", "dosage": 1}
]

# Prise de rendez-vous
rendez_vous = [
    {"id": 1, "patient_id": 1, "date": "2022-03-01", "heure": "10:00"},
    {"id": 2, "patient_id": 2, "date": "2022-03-15", "heure": "14:00"},
    {"id": 3, "patient_id": 3, "date": "2022-04-01", "heure": "18:00"}
]

# Alertes médicaments
alertes = [
    {"id": 1, "patient_id": 1, "medicament": "Ibuprofène", "dernier_usage": "2022-01-01"},
    {"id": 2, "patient_id": 1, "medicament": "Acetaminophène", "dernier_usage": "2022-01-15"},
    {"id": 3, "patient_id": 2, "medicament": "Paracetamol", "dernier_usage": "2022-02-01"}
]

# Dossier médical partagé
dossier = {
    "id": 1,
    "patient_id": 1,
    "fiches": patients,
    "historique": historique,
    "ordonnances": ordonnances,
    "rendez_vous": rendez_vous,
    "alertes": alertes
}

# Graphiques de suivi santé
graphiques = {
    "id": 1,
    "patient_id": 1,
    "graphique1": {
        "label": "Poids",
        "data": [70, 72, 75, 78, 80]
    },
    "graphique2": {
        "label": "Féquence cardiaque",
        "data": [60, 62, 65, 68, 70]
    }
}

# Rapports pour médecins
rapports = {
    "id": 1,
    "patient_id": 1,
    "rapport1": {
        "label": "Consultation",
        "description": "Consultation régulière pour suivre l'état du patient"
    },
    "rapport2": {
        "label": "Analyse de sang",
        "description": "Analyse de sang pour suivre les paramètres du patient"
    }
}

# API en temps réel
@app.route("/api/data", methods=["GET"])
def get_data():
    return json.dumps(dossier)

# Calcul des statistiques/métriques
@app.route("/api/statistiques", methods=["GET"])
def get_statistiques():
    poids = statistics.mean([fiche["poids"] for fiche in patients])
    féquence_cardiaque = statistics.mean([fiche["féquence_cardiaque"] for fiche in patients])
    return f"Poids moyen : {poids}, Féquence cardiaque moyenne : {féquence_cardiaque}"

# Structure modulaire pour différentes visualisations
@app.route("/graphiques", methods=["GET"])
def get_graphiques():
    return render_template("graphiques.html", graphiques=graphiques)

# Interface web
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", patients=patients, historique=historique, ordonnances=ordonnances, rendez_vous=rendez_vous, alertes=alertes)

if __name__ == "__main__":
    app.run(debug=True)
