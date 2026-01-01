python
"""
Application Flask pour To-Do List
"""
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import ToDoForm
from models import db, ToDo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Vue principale de l'application
    """
    form = ToDoForm()
    if form.validate_on_submit():
        todo = ToDo(title=form.title.data, description=form.description.data)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    todos = ToDo.query.all()
    return render_template('index.html', form=form, todos=todos)

@app.route('/detail/<int:todo_id>')
def detail(todo_id):
    """
    Détail d'une tâche
    """
    todo = ToDo.query.get(todo_id)
    if todo is None:
        return 'Tâche introuvable', 404
    try:
        return render_template('detail.html', todo=todo)
    except Exception as e:
        return str(e)

@app.route('/modifier/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def modifier(todo_id):
    """
    Modifier une tâche
    """
    todo = ToDo.query.get(todo_id)
    if todo is None:
        return 'Tâche introuvable', 404
    form = ToDoForm()
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('modifier.html', todo=todo, form=form)

@app.route('/supprimer/<int:todo_id>', methods=['POST'])
@login_required
def supprimer(todo_id):
    """
    Supprimer une tâche
    """
    todo = ToDo.query.get(todo_id)
    if todo is None:
        return 'Tâche introuvable', 404
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

@app.errorhandler(404)
def page_not_found(e):
    return 'Page non trouvée'

if __name__ == '__main__':
    app.run(debug=True)
