from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/create', methods=['POST'])
def create_task():
    title = request.form['title']
    description = request.form['description']
    deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
    priority = int(request.form['priority'])
    task = Task(title=title, description=description, deadline=deadline, priority=priority)
    db.session.add(task)
    db.session.commit()
    return 'Task created'

@app.route('/update', methods=['POST'])
def update_task():
    task_id = int(request.form['id'])
    task = Task.query.get(task_id)
    task.completed = not task.completed
    db.session.commit()
    return 'Task updated'

@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = int(request.form['id'])
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return 'Task deleted'

@app.route('/stats')
def stats():
    tasks = Task.query.all()
    completed = len([t for t in tasks if t.completed])
    total = len(tasks)
    graph_data = {'labels': ['Completed', 'Incomplete'], 'datasets': [{'data': [completed, total - completed]}]}
    return render_template('stats.html', graph_data=graph_data)

@app.route('/filter', methods=['POST'])
def filter_tasks():
    filter_type = request.form['filter_type']
    filter_value = request.form['filter_value']
    if filter_type == 'priority':
        tasks = Task.query.filter_by(priority=filter_value).all()
    elif filter_type == 'deadline':
        deadline = datetime.strptime(filter_value, '%Y-%m-%d')
        tasks = Task.query.filter_by(deadline=deadline).all()
    return render_template('index.html', tasks=tasks)

@app.route('/tri', methods=['POST'])
def tri_tasks():
    tri_type = request.form['tri_type']
    if tri_type == 'title':
        tasks = Task.query.order_by(Task.title).all()
    elif tri_type == 'deadline':
        tasks = Task.query.order_by(Task.deadline).all()
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    with open('data.json', 'w') as f:
        json.dump([{'title': 'Task 1', 'description': 'Description 1', 'deadline': '2024-03-16', 'priority': 1, 'completed': False}, 
                   {'title': 'Task 2', 'description': 'Description 2', 'deadline': '2024-03-17', 'priority': 2, 'completed': True}], f)
    db.create_all()
    app.run(debug=True)
