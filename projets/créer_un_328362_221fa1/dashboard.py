# dashboard.py

import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Données en mémoire
taches = [
    {"id": 1, "nom": "Tâche 1", "statut": "En cours"},
    {"id": 2, "nom": "Tâche 2", "statut": "Terminée"},
    {"id": 3, "nom": "Tâche 3", "statut": "En attente"}
]

# Calcul des statistiques
def calc_statistiques(taches):
    en_cours = len([tache for tache in taches if tache["statut"] == "En cours"])
    terminée = len([tache for tache in taches if tache["statut"] == "Terminée"])
    en_attente = len([tache for tache in taches if tache["statut"] == "En attente"])
    return {
        "en_cours": en_cours,
        "terminée": terminée,
        "en_attente": en_attente
    }

# API pour les données en temps réel
@app.route("/api/taches", methods=["GET"])
def get_taches():
    return jsonify(taches)

@app.route("/api/statistiques", methods=["GET"])
def get_statistiques():
    return jsonify(calc_statistiques(taches))

# Route pour la liste interactive
@app.route("/")
def index():
    statistiques = calc_statistiques(taches)
    return render_template("index.html", taches=taches, statistiques=statistiques)

# Route pour la création de tâches
@app.route("/create", methods=["POST"])
def create_tache():
    id = len(taches) + 1
    nom = request.form["nom"]
    statut = "En cours"
    taches.append({"id": id, "nom": nom, "statut": statut})
    return jsonify({"message": "Tâche créée avec succès"})

# Route pour la gestion de tâches
@app.route("/update/<int:id>", methods=["POST"])
def update_tache(id):
    for tache in taches:
        if tache["id"] == id:
            tache["statut"] = request.form["statut"]
            return jsonify({"message": "Tâche mise à jour avec succès"})
    return jsonify({"message": "Tâche non trouvée"})

# Route pour la suppression de tâches
@app.route("/delete/<int:id>", methods=["POST"])
def delete_tache(id):
    for tache in taches:
        if tache["id"] == id:
            taches.remove(tache)
            return jsonify({"message": "Tâche supprimée avec succès"})
    return jsonify({"message": "Tâche non trouvée"})

if __name__ == "__main__":
    app.run(debug=True)
