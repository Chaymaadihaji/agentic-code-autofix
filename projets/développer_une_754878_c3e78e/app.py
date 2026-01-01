from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Fiches patients détaillées
patients = [
    {"nom": "Jean Dupont", "prenom": "Jean", "date_naissance": "1990-01-01", "telephone": "0612345678"},
    {"nom": "Marie Dupont", "prenom": "Marie", "date_naissance": "1995-02-02", "telephone": "0623456789"}
]

# Historique médical
historique = [
    {"date": "2022-01-01", "medicament": "Ibuprofène", "dosage": "2g"},
    {"date": "2022-02-01", "medicament": "Aspirine", "dosage": "3g"}
]

# Ordonnances numériques
ordonnances = [
    {"date": "2022-01-01", "medicament": "Ibuprofène", "dosage": "2g", "quantite": 10},
    {"date": "2022-02-01", "medicament": "Aspirine", "dosage": "3g", "quantite": 15}
]

# Prise de rendez-vous
rendezVous = [
    {"date": "2022-01-01", "heure": "09:00", "medecin": "Dr. Smith"},
    {"date": "2022-02-01", "heure": "10:00", "medecin": "Dr. Johnson"}
]

# Alertes médicaments
alertes = [
    {"medicament": "Ibuprofène", "alerte": "Risque d'effets secondaires"},
    {"medicament": "Aspirine", "alerte": "Risque d'allergie"}
]

# Dossier médical partagé
dossierMedical = {
    "patient": "Jean Dupont",
    "historique": historique,
    "ordonnances": ordonnances,
    "rendezVous": rendezVous,
    "alertes": alertes
}

# Graphiques de suivi santé
graphiques = {
    "frequences_cardiaques": [80, 85, 90, 88, 82],
    "pressions_arterieles": [120, 125, 130, 128, 122]
}

# Rapports pour médecins
rapports = [
    {"medicament": "Ibuprofène", "dosage": "2g", "quantite": 10},
    {"medicament": "Aspirine", "dosage": "3g", "quantite": 15}
]

# API pour les données en temps réel
@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({
        "patients": patients,
        "historique": historique,
        "ordonnances": ordonnances,
        "rendezVous": rendezVous,
        "alertes": alertes,
        "dossierMedical": dossierMedical,
        "graphiques": graphiques,
        "rapports": rapports
    })

# Calcul des statistiques/métriques
def calcul_statistiques(data):
    # Calcul de la moyenne
    moyenne = sum(data) / len(data)
    return moyenne

# Structure modulaire pour différentes visualisations
class Visualisation:
    def __init__(self, data):
        self.data = data

    def afficher(self):
        # Afficher la visualisation
        print("Visualisation des données")

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
