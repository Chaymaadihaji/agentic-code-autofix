# main.py

import os
from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json
import statistics

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(16)

class TaskForm(FlaskForm):
    task_name = StringField('Nom de la tâche', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class Task:
    def __init__(self, name):
        self.name = name
        self.completed = False

class Dashboard:
    def __init__(self):
        self.tasks = []

    def add_task(self, name):
        self.tasks.append(Task(name))

    def get_stats(self):
        completed = [task for task in self.tasks if task.completed]
        total = len(self.tasks)
        progress = len(completed) / total * 100 if total > 0 else 0
        return {
            'total': total,
            'completed': len(completed),
            'progress': progress
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        dashboard.add_task(form.task_name.data)
        return redirect(url_for('index'))
    return render_template('index.html', form=form, tasks=dashboard.tasks, stats=dashboard.get_stats())

@app.route('/stats')
def stats():
    return jsonify(dashboard.get_stats())

@app.route('/filter', methods=['POST'])
def filter_tasks():
    category = request.json.get('category')
    tasks = [task for task in dashboard.tasks if task.name.startswith(category)]
    return jsonify([task.name for task in tasks])

@app.route('/sort', methods=['POST'])
def sort_tasks():
    order = request.json.get('order')
    tasks = sorted(dashboard.tasks, key=lambda task: task.name, reverse=order == 'desc')
    return jsonify([task.name for task in tasks])

if __name__ == "__main__":
    dashboard = Dashboard()
    app.run(debug=True)

# templates/index.html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1>Dashboard</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.task_name.label }} {{ form.task_name() }}
            </div>
            {{ form.submit() }}
        </form>
        <h2>Tâches</h2>
        <ul>
            {% for task in tasks %}
            <li>{{ task.name }} ({{ 'Oui' if task.completed else 'Non' }})</li>
            {% endfor %}
        </ul>
        <h2>Statistiques</h2>
        <p>Total : {{ stats.total }}</p>
        <p>Complétées : {{ stats.completed }}</p>
        <p>Progression : {{ stats.progress }}%</p>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
