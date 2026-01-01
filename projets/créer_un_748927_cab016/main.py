# main.py

import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# État du jeu
scores = {
    'joueur': 0,
    'ordinateur': 0
}

# Historique des parties
historique = []

# Fonction pour générer les cartes
def generer_cartes():
    return ['pierre', 'papier', 'ciseaux']

# Fonction pour gérer les scores
def gérer_scores(gagnant):
    global scores
    if gagnant == 'joueur':
        scores['joueur'] += 1
    elif gagnant == 'ordinateur':
        scores['ordinateur'] += 1

# Fonction pour déterminer le gagnant
def déterminer_gagnant(joueur, ordinateur):
    if joueur == ordinateur:
        return 'égalité'
    if (joueur == 'pierre' and ordinateur == 'ciseaux') or (joueur == 'papier' and ordinateur == 'pierre') or (joueur == 'ciseaux' and ordinateur == 'papier'):
        return 'joueur'
    return 'ordinateur'

# Fonction pour jouer au jeu
def jouer_jeu():
    global historique
    cartes = generer_cartes()
    joueur = request.form['carte']
    ordinateur = random.choice(cartes)
    gagnant = déterminer_gagnant(joueur, ordinateur)
    gérer_scores(gagnant)
    historique.append({
        'joueur': joueur,
        'ordinateur': ordinateur,
        'gagnant': gagnant
    })
    return gagnant

# Route pour afficher l'interface
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', scores=scores, historique=historique)

# Route pour jouer au jeu
@app.route('/jouer', methods=['POST'])
def jouer():
    return jouer_jeu()

# Lancement de l'app
if __name__ == "__main__":
    app.run(debug=True)
