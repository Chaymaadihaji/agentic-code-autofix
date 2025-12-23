from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import random
import json
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# Génération de données pour le dashboard
donnees = [
    {'nom': 'Tâche 1', 'début': '2022-01-01', 'fin': '2022-01-15', 'statut': 'En cours'},
    {'nom': 'Tâche 2', 'début': '2022-02-01', 'fin': '2022-02-28', 'statut': 'Terminé'},
    {'nom': 'Tâche 3', 'début': '2022-03-01', 'fin': '2022-03-31', 'statut': 'En cours'},
    {'nom': 'Tâche 4', 'début': '2022-04-01', 'fin': '2022-04-30', 'statut': 'Terminé'},
    {'nom': 'Tâche 5', 'début': '2022-05-01', 'fin': '2022-05-31', 'statut': 'En cours'}
]

# Calcul des statistiques/métriques
donnees_df = pd.DataFrame(donnees)
statistiques = {
    'Nombre de tâches en cours': len(donnees_df[donnees_df['statut'] == 'En cours']),
    'Nombre de tâches terminées': len(donnees_df[donnees_df['statut'] == 'Terminé'])
}

# API pour les données en temps réel
@app.route('/api/donnees', methods=['GET'])
def api_donnees():
    return jsonify(donnees)

# Structure modulaire pour différentes visualisations
class Formulaire(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    debut = StringField('Début', validators=[DataRequired()])
    fin = StringField('Fin', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    form = Formulaire()
    if form.validate_on_submit():
        nouvelle_tache = {
            'nom': form.nom.data,
            'début': form.debut.data,
            'fin': form.fin.data,
            'statut': 'En cours'
        }
        donnees.append(nouvelle_tache)
        return jsonify({'message': 'La tâche a été ajoutée avec succès'})
    return render_template('formulaire.html', form=form)

@app.route('/liste', methods=['GET'])
def liste():
    return render_template('liste.html', donnees=donnees)

@app.route('/statistiques', methods=['GET'])
def statistiques_route():
    return render_template('statistiques.html', statistiques=statistiques)

if __name__ == "__main__":
    app.run(debug=True)
