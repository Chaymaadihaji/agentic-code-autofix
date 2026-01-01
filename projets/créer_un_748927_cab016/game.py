# game.py

import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Etat du jeu
scores_p = 0
scores_papier = 0
scores_ciseaux = 0
historique = []

# Fonction pour choisir au hasard
def choisir_hasard():
    return random.choice(['pierre', 'papier', 'ciseaux'])

# Fonction pour vérifier le gagnant
def verifier_gagnant(joueur, ordinateur):
    if joueur == ordinateur:
        return "Egalité"
    if (joueur == 'pierre' and ordinateur == 'ciseaux') or (joueur == 'papier' and ordinateur == 'pierre') or (joueur == 'ciseaux' and ordinateur == 'papier'):
        return "Joueur"
    return "Ordinateur"

# Fonction pour afficher les résultats
def afficher_resultats(joueur, ordinateur, gagnant):
    return {
        'joueur': joueur,
        'ordinateur': ordinateur,
        'gagnant': gagnant
    }

# Route pour jouer
@app.route('/jouer', methods=['POST'])
def jouer():
    joueur = request.form['joueur']
    ordinateur = choisir_hasard()
    gagnant = verifier_gagnant(joueur, ordinateur)
    scores = {
        'pierre': scores_p,
        'papier': scores_papier,
        'ciseaux': scores_ciseaux
    }
    historique.append(afficher_resultats(joueur, ordinateur, gagnant))
    if gagnant == 'Joueur':
        scores[joueur] += 1
    elif gagnant == 'Ordinateur':
        scores[ordinateur] += 1
    return render_template('index.html', scores=scores, historique=historique)

# Route pour afficher le score
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
