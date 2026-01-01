# ui.py

from flask import Flask, render_template, request
import random
import json

app = Flask(__name__)

# Chemin vers le fichier de mots
mots_fichier = 'mots.json'

# Charge les mots au hasard
def charger_mots():
    with open(mots_fichier, 'r') as f:
        mots = json.load(f)['mots']
    return random.choice(mots)

# Génération du mot secret
mot_secret = charger_mots()
tentatives = 4
etat_jeu = {'tentatives': tentatives, 'lettres_utilisees': []}

# Fonction de vérification de la lettre
def verifier_lettre(lettres_utilisees, lettre):
    global tentatives
    global mot_secret
    global etat_jeu
    
    if lettre in mot_secret:
        etat_jeu['lettres_utilisees'].append(lettre)
    else:
        tentatives -= 1
        etat_jeu['tentatives'] = tentatives
        etat_jeu['lettres_utilisees'].append(lettre)

# Fonction de fin de jeu
def fin_jeu(gagne):
    global etat_jeu
    etat_jeu['gagne'] = gagne

# Route pour afficher le formulaire
@app.route('/', methods=['GET'])
def formulaire():
    return render_template('formulaire.html', etat_jeu=etat_jeu)

# Route pour traiter le formulaire
@app.route('/', methods=['POST'])
def traiter_formulaire():
    global mot_secret
    global tentatives
    global etat_jeu
    
    lettre = request.form['lettre']
    verifier_lettre(etat_jeu['lettres_utilisees'], lettre)
    
    if lettre in mot_secret:
        if all([l in etat_jeu['lettres_utilisees'] for l in mot_secret]):
            fin_jeu(True)
    elif tentatives == 0:
        fin_jeu(False)
    
    return render_template('formulaire.html', etat_jeu=etat_jeu)

if __name__ == "__main__":
    app.run(debug=True)
