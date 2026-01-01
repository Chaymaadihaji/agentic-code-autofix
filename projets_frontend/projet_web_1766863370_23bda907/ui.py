# ui.py

import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionnaire de mots à deviner
mots = ["apple", "banana", "cherry", "date", "elderberry"]

# Variable pour stocker la lettre saisie
lettre_saisie = ""

# Variable pour stocker le mot à deviner
mot_a_deviner = random.choice(mots)

# Variable pour stocker le score
score = 0

# Variable pour stocker le nombre d'essais
essais = 6

# Fonction pour générer un mot au hasard
def generer_mot():
    return random.choice(mots)

# Fonction pour vérifier si la lettre est dans le mot
def verifier_lettre(lettre):
    for char in mot_a_deviner:
        if char == lettre:
            return True
    return False

# Fonction pour afficher le résultat
def afficher_resultat():
    resultats = []
    for char in mot_a_deviner:
        if char in lettre_saisie:
            resultats.append(char)
        else:
            resultats.append("_")
    return " ".join(resultats)

# Route pour afficher la page d'accueil
@app.route("/")
def index():
    return render_template("index.html", score=score, essais=essais, mot_a_deviner=mot_a_deviner, lettre_saisie=lettre_saisie)

# Route pour traiter la saisie de la lettre
@app.route("/saisir_lettre", methods=["POST"])
def saisir_lettre():
    global lettre_saisie, mot_a_deviner, score, essais
    lettre = request.form["lettre"]
    if len(lettre) != 1 or not lettre.isalpha():
        return "Veuillez saisir une lettre !"
    if lettre in lettre_saisie:
        return "Vous avez déjà saisir cette lettre !"
    if not verifier_lettre(lettre):
        essais -= 1
        if essais == 0:
            return "Vous avez perdu !"
    else:
        score += 1
    lettre_saisie += lettre
    if "_" not in afficher_resultat():
        return "Vous avez gagné !"
    mot_a_deviner = generer_mot()
    return render_template("index.html", score=score, essais=essais, mot_a_deviner=mot_a_deviner, lettre_saisie=lettre_saisie)

if __name__ == "__main__":
    app.run(debug=True)
