# player.py

import random
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Fichier de données contenant les mots à deviner
with open('mots.json') as f:
    mots = json.load(f)

# État du jeu
etat_jeu = {
    'mot': random.choice(mots),
    'essais': 6,
    'lettres_utilisees': [],
    'score': 0
}

# Fonction de gestion de l'état du jeu
def update_etat_jeu(lettre):
    global etat_jeu
    etat_jeu['lettres_utilisees'].append(lettre)
    if lettre not in etat_jeu['mot']:
        etat_jeu['essais'] -= 1
    if etat_jeu['essais'] == 0:
        etat_jeu['score'] = 0
        etat_jeu['mot'] = random.choice(mots)
        etat_jeu['essais'] = 6
        etat_jeu['lettres_utilisees'] = []
    elif lettre in etat_jeu['mot']:
        etat_jeu['score'] += 1

# Route pour afficher le formulaire
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', etat_jeu=etat_jeu)

# Route pour traiter la saisie de lettre
@app.route('/', methods=['POST'])
def traiter_saisie():
    lettre = request.form['lettre']
    update_etat_jeu(lettre)
    return render_template('index.html', etat_jeu=etat_jeu)

# Route pour afficher le score
@app.route('/score', methods=['GET'])
def afficher_score():
    return render_template('score.html', etat_jeu=etat_jeu)

if __name__ == "__main__":
    app.run(debug=True)
