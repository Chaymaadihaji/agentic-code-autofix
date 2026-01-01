# ui.py

import random
import string
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret_key'

# Dictionnaire de mots au hasard
mots = ['apple', 'banana', 'cherry', 'date', 'elderberry']

# Fonction pour générer un mot au hasard
def generer_mot():
    return random.choice(mots)

# Fonction pour afficher la lettre choisie
def afficher_lettre(mot, lettre):
    mot_list = list(mot)
    for i in range(len(mot)):
        if mot_list[i] == lettre:
            mot_list[i] = lettre.upper()
    return ''.join(mot_list)

# Fonction pour compter le nombre d'essais
def compter_essais(lettre, mot):
    if lettre in mot:
        return 0
    else:
        return 1

# Route pour la page d'accueil
@app.route('/')
def index():
    mot = generer_mot()
    session['mot'] = mot
    session['essais'] = 0
    session['lettres'] = []
    return render_template('index.html')

# Route pour traiter la saisie de la lettre
@app.route('/traiter', methods=['POST'])
def traiter():
    lettre = request.form['lettre']
    mot = session['mot']
    essais = session['essais']
    lettres = session['lettres']
    if lettre in lettres:
        return render_template('index.html', erreur='Vous avez déjà saisi cette lettre !')
    elif lettre in mot:
        mot = afficher_lettre(mot, lettre)
        session['mot'] = mot
        session['lettres'].append(lettre)
    else:
        essais += 1
        session['essais'] = essais
        session['lettres'].append(lettre)
        if essais >= 6:
            return render_template('game_over.html', mot=mot, essais=essais)
    return render_template('index.html', mot=mot, essais=essais)

if __name__ == "__main__":
    app.run(debug=True)
