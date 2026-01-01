# models.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, IntegerField, FloatField
from wtforms.validators import DataRequired
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donnees.db'
db = SQLAlchemy(app)

class Donnee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valeur = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class FormulaireForm(Form):
    valeur = StringField('Valeur', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])

@app.route('/')
def index():
    donnes = Donnee.query.all()
    return render_template('index.html', donnes=donnes)

@app.route('/nouvelle_donnee', methods=['GET', 'POST'])
def nouvelle_donnee():
    form = FormulaireForm(request.form)
    if request.method == 'POST' and form.validate():
        nouvelle_donnee = Donnee(valeur=float(form.valeur.data), date=form.date.data)
        db.session.add(nouvelle_donnee)
        db.session.commit()
        return jsonify({'message': 'Donnée ajoutée avec succès'})
    return render_template('nouvelle_donnee.html', form=form)

@app.route('/graphique')
def graphique():
    donnes = Donnee.query.all()
    valeurs = [d.valeur for d in donnes]
    dates = [d.date for d in donnes]
    return render_template('graphique.html', valeurs=valeurs, dates=dates)

@app.route('/filtrer', methods=['GET', 'POST'])
def filtrer():
    form = FormulaireForm(request.form)
    if request.method == 'POST' and form.validate():
        filtres = request.form
        donnes = Donnee.query.filter_by(**filtres).all()
        return render_template('filtrer.html', donnes=donnes)
    return render_template('filtrer.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return 'Page non trouvée', 404

@app.errorhandler(500)
def internal_server_error(e):
    return 'Erreur interne du serveur', 500

if __name__ == "__main__":
    app.run(debug=True)
