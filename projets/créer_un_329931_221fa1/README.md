from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taches.db'
db = SQLAlchemy(app)

class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Statistique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    nombre_taches = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    taches = Tache.query.all()
    statistiques = Statistique.query.all()
    return render_template('index.html', taches=taches, statistiques=statistiques)

@app.route('/ajouter_tache', methods=['POST'])
def ajouter_tache():
    nom = request.form['nom']
    description = request.form['description']
    tache = Tache(nom=nom, description=description)
    db.session.add(tache)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/filtrer', methods=['POST'])
def filtrer():
    date_debut = request.form['date_debut']
    date_fin = request.form['date_fin']
    taches = Tache.query.filter(Tache.date_creation.between(date_debut, date_fin)).all()
    return render_template('index.html', taches=taches)

@app.route('/tri', methods=['POST'])
def tri():
    ordre = request.form['ordre']
    taches = Tache.query.order_by(ordre).all()
    return render_template('index.html', taches=taches)

if __name__ == '__main__':
    app.run(debug=True)
