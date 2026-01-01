# game.py

import random
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# données de jeu en json
donnees_jeu = json.load(open('donnees_jeu.json'))

# mots à deviner
mots_a_deviner = donnees_jeu['mots_a_deviner']

# état du jeu
etat_jeu = {'mot_a_deviner' : random.choice(mots_a_deviner), 'lettres_proposes' : [], 'essais' : 0, 'score' : 0}

# route pour la page d'accueil
@app.route('/')
def accueil():
    return render_template('accueil.html', etat=etat_jeu)

# route pour la saisie de lettres
@app.route('/saisie', methods=['POST'])
def saisie():
    lettre = request.form['lettre']
    # gérer la saisie de lettres
    if lettre in etat_jeu['mot_a_deviner']:
        # lettre correcte
        etat_jeu['lettres_proposes'].append(lettre)
        etat_jeu['score'] += 1
    else:
        # lettre incorrecte
        etat_jeu['essais'] += 1
    return render_template('saisie.html', etat=etat_jeu)

# route pour l'affichage des résultats
@app.route('/resultats')
def resultats():
    return render_template('resultats.html', etat=etat_jeu)

# lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
