import os
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
Bootstrap(app)

# Données pour le dashboard
tasks = [
    {"id": 1, "name": "Tâche 1", "état": "En cours"},
    {"id": 2, "name": "Tâche 2", "état": "Terminée"},
    {"id": 3, "name": "Tâche 3", "état": "En cours"}
]

# Fonction pour générer des données aléatoires
def generate_data():
    for i in range(10):
        tasks.append({
            "id": i+4,
            "name": f"Tâche {i+4}",
            "état": "En cours" if i % 2 == 0 else "Terminée"
        })

# Calcul des statistiques
def calc_statistiques(tasks):
    total = len(tasks)
    en_cours = sum(1 for task in tasks if task["état"] == "En cours")
    terminée = total - en_cours
    return total, en_cours, terminée

# API pour les données en temps réel
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# API pour les statistiques
@app.route('/api/statistiques', methods=['GET'])
def get_statistiques():
    total, en_cours, terminée = calc_statistiques(tasks)
    return jsonify({
        "total": total,
        "en_cours": en_cours,
        "terminée": terminée
    })

# Route pour la page d'accueil
@app.route('/', methods=['GET'])
def index():
    total, en_cours, terminée = calc_statistiques(tasks)
    return render_template('index.html', tasks=tasks, total=total, en_cours=en_cours, terminée=terminée)

# Fonction pour mettre à jour la liste des tâches
@app.route('/update_tasks', methods=['POST'])
def update_tasks():
    id = request.form['id']
    état = request.form['état']
    for task in tasks:
        if task['id'] == int(id):
            task['état'] = état
    return jsonify({"message": "Tâche mise à jour avec succès"})

# Fonction pour ajouter une nouvelle tâche
@app.route('/add_task', methods=['POST'])
def add_task():
    name = request.form['name']
    tasks.append({
        "id": len(tasks) + 1,
        "name": name,
        "état": "En cours"
    })
    return jsonify({"message": "Tâche ajoutée avec succès"})

if __name__ == "__main__":
    app.run(debug=True)

# Template HTML
from flask import render_template
@app.context_processor
def inject_template():
    return dict(total=0, en_cours=0, terminée=0)

@app.route('/template')
def template():
    return render_template('template.html', total=0, en_cours=0, terminée=0)

# Fichier de configuration pour Bootstrap
with open('static/config.json', 'w') as f:
    json.dump({
        "version": "1.0",
        "bootstrap": "5.1.3",
        "font_awesome": "5.15.3"
    }, f)
