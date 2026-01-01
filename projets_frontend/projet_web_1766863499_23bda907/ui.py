import random
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Chargement des mots à deviner
with open('mots.json') as f:
    mots = json.load(f)

# Etat du jeu
etat_jeu = {
    'mots': mots,
    'mot_a_deviner': '',
    'lettres_utilisees': [],
    'score': 0,
    'niveau': 1
}

@app.route('/')
def index():
    return render_template('index.html', etat_jeu=etat_jeu)

@app.route('/devine', methods=['POST'])
def devine():
    lettre = request.form['lettre']
    # Génération du mot à deviner
    etat_jeu['mot_a_deviner'] = random.choice(etat_jeu['mots']['niveau' + str(etat_jeu['niveau'])])
    # Vérification de la lettre
    if lettre in etat_jeu['mot_a_deviner']:
        etat_jeu['score'] += 10
    else:
        etat_jeu['lettres_utilisees'].append(lettre)
        etat_jeu['score'] -= 10
    # Affichage du pendu
    etat_jeu['pendu'] = affiche_pendu(etat_jeu['lettres_utilisees'])
    return jsonify(etat_jeu)

@app.route('/niveau', methods=['POST'])
def niveau():
    etat_jeu['niveau'] += 1
    return jsonify(etat_jeu)

def affiche_pendu(lettres_utilisees):
    pendu = ''
    for i in range(len(etat_jeu['mot_a_deviner'])):
        if etat_jeu['mot_a_deviner'][i] in lettres_utilisees:
            pendu += '_'
        else:
            pendu += etat_jeu['mot_a_deviner'][i]
    return pendu

if __name__ == "__main__":
    app.run(debug=True)
