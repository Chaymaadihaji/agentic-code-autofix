import random
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Liste de mots à deviner
mots = ["orange", "maison", "ordinateur", "papier", "plume"]

# Structure de données pour l'état du jeu
etat_jeu = {
    "mot_secret": random.choice(mots),
    "lettres_utilisees": "",
    "essais": 6,
    "score": 0
}

# Génération de mots au hasard
def generer_mot():
    return random.choice(mots)

# Affichage du pendu
def afficher_pendu(essais):
    if essais == 6:
        return "_______\n|       |\n|       |\n|       |\n|       |\n|       |"
    elif essais == 5:
        return "_______\n|       |\n|   O   |\n|       |\n|       |\n|       |"
    elif essais == 4:
        return "_______\n|       |\n|   O   |\n|   |   |\n|       |\n|       |"
    elif essais == 3:
        return "_______\n|       |\n|   O   |\n|  /|   |\n|       |\n|       |"
    elif essais == 2:
        return "_______\n|       |\n|   O   |\n|  /|\  |\n|       |\n|       |"
    elif essais == 1:
        return "_______\n|       |\n|   O   |\n|  /|\ \|\n|       |\n|       |"
    else:
        return "_______\n|       |\n|   O   |\n|  /|\ \|\n|  /    \n|_____|"

# Saisie de lettres par l'utilisateur
@app.route('/', methods=['GET', 'POST'])
def saisie_litterre():
    global etat_jeu
    if request.method == 'POST':
        lettre = request.form['lettre']
        if lettre in etat_jeu['mot_secret']:
            etat_jeu['lettres_utilisees'] += lettre
            for i in range(len(etat_jeu['mot_secret'])):
                if etat_jeu['mot_secret'][i] == lettre:
                    etat_jeu['mot_secret'] = etat_jeu['mot_secret'][:i] + "*" + etat_jeu['mot_secret'][i+1:]
        else:
            etat_jeu['essais'] -= 1
            etat_jeu['lettres_utilisees'] += lettre
        if '*' not in etat_jeu['mot_secret']:
            etat_jeu['score'] += 10
            return render_template('win.html', mot=etat_jeu['mot_secret'], score=etat_jeu['score'])
        elif etat_jeu['essais'] == 0:
            etat_jeu['score'] -= 10
            return render_template('lose.html', mot=etat_jeu['mot_secret'], score=etat_jeu['score'])
    return render_template('index.html', pendu=afficher_pendu(etat_jeu['essais']), lettre_utilisees=etat_jeu['lettres_utilisees'], score=etat_jeu['score'])

@app.route('/restart', methods=['GET'])
def restart():
    global etat_jeu
    etat_jeu = {
        "mot_secret": generer_mot(),
        "lettres_utilisees": "",
        "essais": 6,
        "score": 0
    }
    return render_template('index.html', pendu=afficher_pendu(etat_jeu['essais']), lettre_utilisees=etat_jeu['lettres_utilisees'], score=etat_jeu['score'])

if __name__ == "__main__":
    app.run(debug=True)
