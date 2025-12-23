from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taches.db'
db = SQLAlchemy(app)

class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cree_le = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    modifie_le = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(128), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/taches', methods=['GET', 'POST'])
def taches():
    if request.method == 'POST':
        tache = Tache(nom=request.form['nom'], description=request.form['description'])
        db.session.add(tache)
        db.session.commit()
    taches = Tache.query.all()
    return render_template('taches.html', taches=taches)

@app.route('/tache/<int:id>', methods=['GET', 'POST'])
def tache(id):
    tache = Tache.query.get(id)
    if request.method == 'POST':
        tache.nom = request.form['nom']
        tache.description = request.form['description']
        db.session.commit()
    return render_template('tache.html', tache=tache)

@app.route('/statistiques')
def statistiques():
    taches = Tache.query.all()
    nombres = [tache.id for tache in taches]
    nombres.append(0)
    return render_template('statistiques.html', nombres=nombres)

if __name__ == '__main__':
    app.run(debug=True)
