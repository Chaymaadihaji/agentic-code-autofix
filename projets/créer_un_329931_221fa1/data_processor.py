# data_processor.py

import json
import os
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

app = Flask(__name__)

# Génération de données pour le dashboard
data = {
    "tâches": [
        {"nom": "Tâche 1", "statut": "En cours", "début": "2022-01-01", "fin": "2022-01-15"},
        {"nom": "Tâche 2", "statut": "Terminée", "début": "2022-02-01", "fin": "2022-02-28"},
        {"nom": "Tâche 3", "statut": "En cours", "début": "2022-03-01", "fin": "2022-03-31"},
        {"nom": "Tâche 4", "statut": "Terminée", "début": "2022-04-01", "fin": "2022-04-30"},
        {"nom": "Tâche 5", "statut": "En cours", "début": "2022-05-01", "fin": "2022-05-31"}
    ]
}

# Chargement des données depuis un fichier JSON
def charger_donnees():
    if os.path.exists("donnees.json"):
        with open("donnees.json", "r") as f:
            return json.load(f)
    else:
        return data

# Enregistrement des données dans un fichier JSON
def enregistrer_donnees(donnees):
    with open("donnees.json", "w") as f:
        json.dump(donnees, f)

# Création de la base de données
@app.route("/donnees", methods=["GET"])
def get_donnees():
    donnees = charger_donnees()
    return jsonify(donnees)

# Ajout d'une nouvelle tâche
@app.route("/donnees", methods=["POST"])
def ajouter_tache():
    donnees = charger_donnees()
    new_tache = {
        "nom": request.json["nom"],
        "statut": "En cours",
        "début": request.json["début"],
        "fin": request.json["fin"]
    }
    donnees["tâches"].append(new_tache)
    enregistrer_donnees(donnees)
    return jsonify(new_tache)

# Mise à jour d'une tâche existante
@app.route("/donnees/<int:id>", methods=["PUT"])
def mettre_a_jour_tache(id):
    donnees = charger_donnees()
    for tache in donnees["tâches"]:
        if tache["id"] == id:
            tache["nom"] = request.json["nom"]
            tache["statut"] = request.json["statut"]
            tache["début"] = request.json["début"]
            tache["fin"] = request.json["fin"]
            enregistrer_donnees(donnees)
            return jsonify(tache)
    return jsonify({"erreur": "Tâche non trouvée"})

# Suppression d'une tâche
@app.route("/donnees/<int:id>", methods=["DELETE"])
def supprimer_tache(id):
    donnees = charger_donnees()
    for i, tache in enumerate(donnees["tâches"]):
        if tache["id"] == id:
            del donnees["tâches"][i]
            enregistrer_donnees(donnees)
            return jsonify({"message": "Tâche supprimée"})
    return jsonify({"erreur": "Tâche non trouvée"})

# Calcul des statistiques de progression
@app.route("/statistiques", methods=["GET"])
def get_statistiques():
    donnees = charger_donnees()
    taches_en_cours = [tache for tache in donnees["tâches"] if tache["statut"] == "En cours"]
    taches_terminees = [tache for tache in donnees["tâches"] if tache["statut"] == "Terminée"]
    return jsonify({
        "taches_en_cours": len(taches_en_cours),
        "taches_terminees": len(taches_terminees)
    })

# Lancement de l'app
if __name__ == "__main__":
    app.run(debug=True)
