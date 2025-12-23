# data_processor.py

import json
import random
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Structure de données
donnees = {
    "taches": [
        {"id": 1, "nom": "Tâche 1", "statut": "En cours"},
        {"id": 2, "nom": "Tâche 2", "statut": "Terminée"},
        {"id": 3, "nom": "Tâche 3", "statut": "En cours"}
    ],
    "statistiques": {
        "total": 3,
        "en_cours": 2,
        "terminées": 1
    }
}

# Fonction de génération de données
def generer_donnees():
    donnees["taches"] = [
        {"id": i, "nom": f"Tâche {i}", "statut": random.choice(["En cours", "Terminée"])} for i in range(1, 4)
    ]
    donnees["statistiques"]["total"] = len(donnees["taches"])
    donnees["statistiques"]["en_cours"] = sum(1 for tache in donnees["taches"] if tache["statut"] == "En cours")
    donnees["statistiques"]["terminées"] = len(donnees["taches"]) - donnees["statistiques"]["en_cours"]

# API pour les données en temps réel
@app.route("/donnees", methods=["GET"])
def obtenir_donnees():
    return jsonify(donnees)

# Route pour la liste interactive
@app.route("/liste_taches", methods=["GET"])
def liste_taches():
    return render_template("liste_taches.html", donnees=donnees)

# Route pour la création de tâches
@app.route("/creer_tache", methods=["POST"])
def creer_tache():
    donnees["taches"].append({"id": len(donnees["taches"]) + 1, "nom": "Tâche nouvelle", "statut": "En cours"})
    generer_donnees()
    return jsonify(donnees)

# Route pour la gestion de tâches
@app.route("/gestion_taches", methods=["POST"])
def gestion_taches():
    id_tache = int(request.form["id_tache"])
    statut = request.form["statut"]
    for tache in donnees["taches"]:
        if tache["id"] == id_tache:
            tache["statut"] = statut
            break
    generer_donnees()
    return jsonify(donnees)

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)

# Template HTML
from flask import render_template
from data_processor import donnees

@app.route("/")
def index():
    return render_template("index.html", donnees=donnees)
