# main.py

from flask import Flask, render_template, request
import random
import json

app = Flask(__name__)

# Données pour le jeu
mots_a_deviner = ["paysage", "informatique", "python", "developpement"]
score = 0
niveau = 1
mot_a_deviner = random.choice(mots_a_deviner)
champs = ["_"] * len(mot_a_deviner)
erreurs = 0

# Fonction pour afficher le mot à deviner
def afficher_mot_a_deviner():
    return "".join(champs)

# Fonction pour vérifier si la lettre est présente dans le mot à deviner
def verifier_lettre(lettre):
    global score
    global niveau
    global mot_a_deviner
    global champs
    global erreurs
    for i in range(len(mot_a_deviner)):
        if mot_a_deviner[i] == lettre:
            champs[i] = lettre
    if "_" not in champs:
        score += 10 * niveau
        niveau += 1
        mot_a_deviner = random.choice(mots_a_deviner)
        champs = ["_"] * len(mot_a_deviner)
    elif lettre not in mot_a_deviner:
        erreurs += 1
        if erreurs == 4:
            return False
    return True

# Fonction pour générer le HTML
@app.route("/", methods=["GET", "POST"])
def index():
    global score
    global niveau
    global mot_a_deviner
    global champs
    global erreurs
    if request.method == "POST":
        lettre = request.form["lettre"]
        if verifier_lettre(lettre):
            return render_template("index.html", champ=afficher_mot_a_deviner(), score=score, niveau=niveau, erreurs=erreurs)
        else:
            return render_template("game_over.html", score=score, erreurs=erreurs)
    return render_template("index.html", champ=afficher_mot_a_deviner(), score=score, niveau=niveau, erreurs=erreurs)

if __name__ == "__main__":
    app.run(debug=True)
