import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flaskbootstrap import Bootstrap
from werkzeug.utils import secure_filename
import json
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# Modèle de tâche
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

# Fonction pour générer des données de démo
def generate_demo_data():
    tasks = []
    for i in range(10):
        title = f'Tâche {i+1}'
        description = f'Décription de la tâche {i+1}'
        tasks.append(Task(title=title, description=description))
    db.session.add_all(tasks)
    db.session.commit()

# Calcul des statistiques
def calculate_stats(tasks):
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.completed])
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress': (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    }

# API pour les données en temps réel
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks])

# Route pour la liste interactive des tâches
@app.route('/')
def index():
    tasks = Task.query.all()
    stats = calculate_stats(tasks)
    return render_template('index.html', tasks=tasks, stats=stats)

# Route pour la création, modification et suppression de tâches
@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.form['title']
    description = request.form['description']
    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Tâche créée avec succès'})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'message': 'Tâche mise à jour avec succès'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tâche supprimée avec succès'})

if __name__ == "__main__":
    generate_demo_data()
    app.run(debug=True)
