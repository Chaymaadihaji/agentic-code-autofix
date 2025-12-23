import os
from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Génération de données pour le dashboard
with open('data.json', 'w') as f:
    data = {
        "tasks": [
            {"id": 1, "title": "Tâche 1", "description": "Description de la tâche 1", "status": "en cours"},
            {"id": 2, "title": "Tâche 2", "description": "Description de la tâche 2", "status": "terminée"},
            {"id": 3, "title": "Tâche 3", "description": "Description de la tâche 3", "status": "en cours"},
        ]
    }
    json.dump(data, f)

# Calcul des statistiques/métriques
def calculate_stats(tasks):
    stats = {
        "total": len(tasks),
        "en_cours": len([t for t in tasks if t['status'] == "en cours"]),
        "terminées": len([t for t in tasks if t['status'] == "terminée"]),
        "en_attente": len([t for t in tasks if t['status'] == "en attente"]),
    }
    return stats

# API pour les données en temps réel
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data['tasks'])

# Gestion des erreurs de base
@app.errorhandler(404)
def not_found(e):
    return 'Page not found', 404

# Route pour la page d'accueil
@app.route('/')
def index():
    with open('data.json', 'r') as f:
        data = json.load(f)
    stats = calculate_stats(data['tasks'])
    return render_template('index.html', tasks=data['tasks'], stats=stats)

# Route pour la création de tâches
@app.route('/create-task', methods=['POST'])
def create_task():
    with open('data.json', 'r') as f:
        data = json.load(f)
    new_task = {
        "id": len(data['tasks']) + 1,
        "title": request.form['title'],
        "description": request.form['description'],
        "status": request.form['status'],
    }
    data['tasks'].append(new_task)
    with open('data.json', 'w') as f:
        json.dump(data, f)
    return jsonify({'message': 'Tâche créée avec succès'})

# Route pour la mise à jour de tâches
@app.route('/update-task', methods=['POST'])
def update_task():
    with open('data.json', 'r') as f:
        data = json.load(f)
    task_id = request.form['id']
    task = next((t for t in data['tasks'] if t['id'] == task_id), None)
    if task:
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        task['status'] = request.form['status']
        with open('data.json', 'w') as f:
            json.dump(data, f)
        return jsonify({'message': 'Tâche mise à jour avec succès'})
    return jsonify({'message': 'Tâche non trouvée'}), 404

# Route pour la suppression de tâches
@app.route('/delete-task', methods=['POST'])
def delete_task():
    with open('data.json', 'r') as f:
        data = json.load(f)
    task_id = request.form['id']
    data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
    with open('data.json', 'w') as f:
        json.dump(data, f)
    return jsonify({'message': 'Tâche supprimée avec succès'})

if __name__ == "__main__":
    app.run(debug=True)
