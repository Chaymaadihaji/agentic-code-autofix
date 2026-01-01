import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

# Liste de mots pour le jeu
mots = ["apple", "banana", "cherry", "date", "elderberry"]

# État du jeu
etat_jeu = {
    "mot_secrete": "",
    "lettres_utilisees": [],
    "erreurs": 0,
    "score": 0
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nouveau_jeu", methods=["POST"])
def nouveau_jeu():
    global etat_jeu
    etat_jeu = {
        "mot_secrete": random.choice(mots),
        "lettres_utilisees": [],
        "erreurs": 0,
        "score": 0
    }
    return render_template("jeu.html", etat_jeu=etat_jeu)

@app.route("/essai", methods=["POST"])
def essai():
    global etat_jeu
    lettre = request.form["lettre"]
    if lettre in etat_jeu["mot_secrete"]:
        etat_jeu["score"] += 1
    else:
        etat_jeu["erreurs"] += 1
    etat_jeu["lettres_utilisees"].append(lettre)
    return render_template("jeu.html", etat_jeu=etat_jeu)

@app.route("/score")
def score():
    global etat_jeu
    return render_template("score.html", etat_jeu=etat_jeu)

if __name__ == "__main__":
    app.run(debug=True)
