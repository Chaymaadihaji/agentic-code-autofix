python
# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    """Classe représentant une tâche à effectuer."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Task {self.title}>'

class TodoList:
    def __init__(self, app):
        self.app = app
        self.db = self.init_db()

    def init_db(self):
        db.init_app(self.app)
        return db

    def get_tasks(self):
        try:
            tasks = Task.query.all()
            return [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
        except Exception as e:
            return str(e)

    def add_task(self, title, description=None):
        try:
            task = Task(title=title, description=description, completed=False)
            db.session.add(task)
            db.session.commit()
            return {"id": task.id, "title": task.title, "completed": task.completed}
        except Exception as e:
            db.session.rollback()
            return str(e)

    def update_task(self, id, title=None, description=None, completed=None):
        try:
            task = Task.query.get(id)
            if title:
                task.title = title
            if description:
                task.description = description
            if completed is not None:
                task.completed = completed
            db.session.commit()
            return {"id": task.id, "title": task.title, "completed": task.completed}
        except Exception as e:
            db.session.rollback()
            return str(e)

    def delete_task(self, id):
        try:
            task = Task.query.get(id)
            db.session.delete(task)
            db.session.commit()
            return True
        except Exception as e:
            return str(e)
