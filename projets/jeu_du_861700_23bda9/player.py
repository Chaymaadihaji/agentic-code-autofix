import random
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Données pour le jeu du pendu
mots = ["papillon", "tigre", "ours", "éléphant", "lion"]
score = 0
tentatives = 4
etat_jeu = {
    "mot": "",
    "tentatives": tentatives,
    "score": score
}

# Chargement du mot au hasard
def charger_mot():
    global mot
    mot = random.choice(mots)
    etat_jeu["mot"] = "*" * len(mot)

# Logique de jeu
def jouer(lettre):
    global tentatives, score
    if lettre in mot:
        etat_jeu["mot"] = "".join([c if c == lettre else "*" for c in mot])
        if "*" not in etat_jeu["mot"]:
            score += 1
            tentatives = 4
    else:
        tentatives -= 1
    etat_jeu["tentatives"] = tentatives

# Interface Flask
@app.route("/")
def index():
    return render_template("index.html", etat_jeu=etat_jeu)

@app.route("/jouer", methods=["POST"])
def jouer_action():
    lettre = request.form["lettre"]
    jouer(lettre)
    return render_template("index.html", etat_jeu=etat_jeu)

@app.route("/reset")
def reset():
    global score, tentatives, mot
    score = 0
    tentatives = 4
    mot = ""
    charger_mot()
    return render_template("index.html", etat_jeu=etat_jeu)

if __name__ == "__main__":
    charger_mot()
    app.run(debug=True)
