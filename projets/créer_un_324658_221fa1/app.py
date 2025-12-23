from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import json
import random

app = Flask(__name__)
Bootstrap(app)

# Données de tâches en mémoire
taches = [
    {"id": 1, "titre": "Tâche 1", "description": "Description de la tâche 1", "etat": "en_cours"},
    {"id": 2, "titre": "Tâche 2", "description": "Description de la tâche 2", "etat": "termine"},
    {"id": 3, "titre": "Tâche 3", "description": "Description de la tâche 3", "etat": "en_cours"}
]

# API pour les données en temps réel
@app.route('/api/taches', methods=['GET'])
def get_taches():
    return jsonify(taches)

# Création de tâches
@app.route('/creer_tache', methods=['POST'])
def creer_tache():
    nouvelle_tache = {
        "id": len(taches) + 1,
        "titre": request.form['titre'],
        "description": request.form['description'],
        "etat": "en_cours"
    }
    taches.append(nouvelle_tache)
    return jsonify(nouvelle_tache)

# Édition de tâches
@app.route('/editer_tache/<int:id>', methods=['PUT'])
def editer_tache(id):
    for tache in taches:
        if tache['id'] == id:
            tache['titre'] = request.form['titre']
            tache['description'] = request.form['description']
            return jsonify(tache)
    return jsonify({"erreur": "Tâche non trouvée"})

# Suppression de tâches
@app.route('/supprimer_tache/<int:id>', methods=['DELETE'])
def supprimer_tache(id):
    for tache in taches:
        if tache['id'] == id:
            taches.remove(tache)
            return jsonify({"message": "Tâche supprimée"})
    return jsonify({"erreur": "Tâche non trouvée"})

# Affichage de statistiques de progression
@app.route('/statistiques', methods=['GET'])
def statistiques():
    en_cours = len([tache for tache in taches if tache['etat'] == 'en_cours'])
    termine = len([tache for tache in taches if tache['etat'] == 'termine'])
    return jsonify({"en_cours": en_cours, "termine": termine})

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html', taches=taches)

# Page de création de tâches
@app.route('/creer')
def creer():
    return render_template('creer.html')

# Page de visualisation des tâches
@app.route('/visualiser')
def visualiser():
    return render_template('visualiser.html', taches=taches)

if __name__ == "__main__":
    app.run(debug=True)
