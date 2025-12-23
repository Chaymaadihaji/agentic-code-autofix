# dashboard.py

import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Génération de données pour le dashboard
donnees = {
    "taches": [
        {"id": 1, "nom": "Tâche 1", "etat": "en cours", "progression": 20},
        {"id": 2, "nom": "Tâche 2", "etat": "terminée", "progression": 100},
        {"id": 3, "nom": "Tâche 3", "etat": "en attente", "progression": 0},
        {"id": 4, "nom": "Tâche 4", "etat": "en cours", "progression": 50},
        {"id": 5, "nom": "Tâche 5", "etat": "terminée", "progression": 100},
    ],
    "stats": {
        "nombre_taches": len(donnees["taches"]),
        "taches_en_cours": len([tache for tache in donnees["taches"] if tache["etat"] == "en cours"]),
        "taches_terminées": len([tache for tache in donnees["taches"] if tache["etat"] == "terminée"]),
        "taches_en_attente": len([tache for tache in donnees["taches"] if tache["etat"] == "en attente"]),
    },
}

# API pour les données en temps réel
@app.route("/api/donnees", methods=["GET"])
def get_donnees():
    return jsonify(donnees)

# Structure modulaire pour différentes visualisations
@app.route("/")
def index():
    return render_template("index.html", donnees=donnees)

# Fonction pour créer une nouvelle tâche
@app.route("/creer_tache", methods=["POST"])
def creer_tache():
    new_tache = {
        "id": len(donnees["taches"]) + 1,
        "nom": request.form["nom"],
        "etat": "en cours",
        "progression": 0,
    }
    donnees["taches"].append(new_tache)
    return jsonify(new_tache)

# Fonction pour mettre à jour la progression d'une tâche
@app.route("/mettre_a_jour_progression", methods=["POST"])
def mettre_a_jour_progression():
    id_tache = request.form["id"]
    progression = request.form["progression"]
    for tache in donnees["taches"]:
        if tache["id"] == int(id_tache):
            tache["progression"] = int(progression)
            break
    return jsonify({"message": "Progression mise à jour avec succès"})

# Lancement de l'app
if __name__ == "__main__":
    app.run(debug=True)
