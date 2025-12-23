# data_processor.py

import json
import random
from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Structure de données
taches = [
    {"id": 1, "nom": "Tâche 1", "etat": True},
    {"id": 2, "nom": "Tâche 2", "etat": False},
    {"id": 3, "nom": "Tâche 3", "etat": True},
]

# Génération de données
def generer_taches(n):
    return [{"id": i, "nom": f"Tâche {i}", "etat": random.choice([True, False])} for i in range(1, n+1)]

# Calcul des statistiques
def calculer_statistiques(taches):
    total_taches = len(taches)
    taches_terminees = sum(1 for tache in taches if tache["etat"])
    return {
        "total_taches": total_taches,
        "taches_terminees": taches_terminees,
        "progres": (taches_terminees / total_taches) * 100,
    }

# API pour les données en temps réel
@app.route("/api/taches", methods=["GET"])
def get_taches():
    return jsonify(taches)

@app.route("/api/taches", methods=["POST"])
def ajouter_tache():
    nouveau_id = max(tache["id"] for tache in taches) + 1
    nouvelle_tache = {"id": nouveau_id, "nom": request.json["nom"], "etat": request.json.get("etat", False)}
    taches.append(nouvelle_tache)
    return jsonify(nouvelle_tache)

@app.route("/api/taches", methods=["DELETE"])
def supprimer_tache():
    id_tache = request.json["id"]
    taches = [tache for tache in taches if tache["id"] != id_tache]
    return jsonify({"message": "Tâche supprimée"})

# Route pour le dashboard
@app.route("/")
def index():
    statistiques = calculer_statistiques(taches)
    return render_template("index.html", statistiques=statistiques)

if __name__ == "__main__":
    app.run(debug=True)
