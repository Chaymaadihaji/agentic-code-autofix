# data_processor.py
import random
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Simuler des données pour le dashboard
data = [
    {"id": 1, "nom": "Tâche 1", "état": "en cours", "progression": 50},
    {"id": 2, "nom": "Tâche 2", "état": "terminé", "progression": 100},
    {"id": 3, "nom": "Tâche 3", "état": "en cours", "progression": 75},
]

# API pour les données en temps réel
@app.route('/data', methods=['GET'])
def get_data():
    return json.dumps(data)

# Calcul des statistiques/métriques
@app.route('/stats', methods=['GET'])
def get_stats():
    stats = {
        "taches_en_cours": len([tache for tache in data if tache["état"] == "en cours"]),
        "taches_termines": len([tache for tache in data if tache["état"] == "terminé"]),
        "moyenne_progression": sum([tache["progression"] for tache in data]) / len(data)
    }
    return json.dumps(stats)

# Création, modification et suppression de tâches
@app.route('/tache', methods=['POST'])
def create_tache():
    new_tache = {
        "id": len(data) + 1,
        "nom": request.json["nom"],
        "état": "en cours",
        "progression": random.randint(0, 100)
    }
    data.append(new_tache)
    return json.dumps(new_tache)

@app.route('/tache/<int:id>', methods=['PUT'])
def update_tache(id):
    for tache in data:
        if tache["id"] == id:
            tache["nom"] = request.json["nom"]
            tache["état"] = request.json["état"]
            tache["progression"] = request.json["progression"]
            return json.dumps(tache)
    return "Tâche non trouvée", 404

@app.route('/tache/<int:id>', methods=['DELETE'])
def delete_tache(id):
    global data
    data = [tache for tache in data if tache["id"] != id]
    return "Tâche supprimée"

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
