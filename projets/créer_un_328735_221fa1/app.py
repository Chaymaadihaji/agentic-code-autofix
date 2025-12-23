# app.py

from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json
import random

app = Flask(__name__)
Bootstrap(app)

# Structure de données pour le dashboard
tâches = [
    {"id": 1, "nom": "Tâche 1", "statut": "en cours"},
    {"id": 2, "nom": "Tâche 2", "statut": "terminée"},
    {"id": 3, "nom": "Tâche 3", "statut": "en cours"}
]

# API pour les données en temps réel
@app.route("/api/tâches", methods=["GET"])
def api_tâches():
    return jsonify(tâches)

# Route pour la liste interactive des tâches
@app.route("/tâches", methods=["GET", "POST"])
def tâches_liste():
    if request.method == "POST":
        nom = request.form["nom"]
        statut = request.form["statut"]
        tâche = {"id": len(tâches) + 1, "nom": nom, "statut": statut}
        tâches.append(tâche)
        return jsonify(tâches)
    return render_template("tâches.html", tâches=tâches)

# Route pour la création, modification et suppression de tâches
@app.route("/tâche/<int:id>", methods=["GET", "PUT", "DELETE"])
def tâche(id):
    for tâche in tâches:
        if tâche["id"] == id:
            if request.method == "PUT":
                tâche["nom"] = request.json["nom"]
                tâche["statut"] = request.json["statut"]
                return jsonify(tâche)
            elif request.method == "DELETE":
                tâches.remove(tâche)
                return jsonify({"message": "Tâche supprimée"})
            return jsonify(tâche)
    return jsonify({"message": "Tâche non trouvée"})

# Route pour les statistiques de progression
@app.route("/statistiques", methods=["GET"])
def statistiques():
    en_cours = [tâche for tâche in tâches if tâche["statut"] == "en cours"]
    terminées = [tâche for tâche in tâches if tâche["statut"] == "terminée"]
    return jsonify({"en_cours": len(en_cours), "terminées": len(terminées)})

# Route pour la galerie
@app.route("/galerie", methods=["GET"])
def galerie():
    return render_template("galerie.html")

# Route pour le dashboard
@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

# Structure modulaire pour différentes visualisations
@app.route("/graphiques", methods=["GET"])
def graphiques():
    return render_template("graphiques.html")

if __name__ == "__main__":
    app.run(debug=True)
