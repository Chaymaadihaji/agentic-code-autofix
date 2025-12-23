from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Dashboard:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()
        self.tasks.append(task)

    def get_tasks(self):
        return Task.query.all()

    def get_statistics(self):
        completed_tasks = Task.query.filter_by(completed=True).count()
        total_tasks = Task.query.count()
        return {
            "completed": completed_tasks,
            "total": total_tasks,
            "progress": completed_tasks / total_tasks * 100 if total_tasks > 0 else 0
        }

    def filter_tasks(self, status):
        return Task.query.filter_by(completed=status).all()

    def get_filtered_stats(self, status):
        tasks = self.filter_tasks(status)
        return {
            "completed": len(tasks),
            "total": len(tasks),
            "progress": 100 if status else 0
        }

dashboard = Dashboard()

@app.route("/")
def index():
    tasks = dashboard.get_tasks()
    stats = dashboard.get_statistics()
    return render_template("index.html", tasks=tasks, stats=stats)

@app.route("/add-task", methods=["POST"])
def add_task():
    title = request.json["title"]
    dashboard.add_task(title)
    return jsonify({"message": "Task added successfully"})

@app.route("/filter-tasks", methods=["POST"])
def filter_tasks():
    status = request.json["status"]
    tasks = dashboard.filter_tasks(status)
    stats = dashboard.get_filtered_stats(status)
    return jsonify({"tasks": [task.title for task in tasks], "stats": stats})

@app.route("/stats")
def get_stats():
    stats = dashboard.get_statistics()
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
