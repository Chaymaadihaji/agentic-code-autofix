from flask import Flask, render_template, request
from random import choice
import string

app = Flask(__name__)

# Liste de mots à deviner
mots = ["apple", "banana", "cherry", "date", "elderberry"]

# Mot à deviner aléatoire
mot_secret = choice(mots)

# Liste des lettres saisies
lettres_saisies = []

@app.route("/")
def index():
    return render_template("index.html", mot_secret=mot_secret, lettres_saisies=lettres_saisies)

@app.route("/saisie", methods=["POST"])
def saisie():
    lettre = request.form["lettre"]
    if lettre in mot_secret:
        # La lettre est dans le mot
        pass
    else:
        # La lettre n'est pas dans le mot
        pass
    # Mise à jour de la liste des lettres saisies
    lettres_saisies.append(lettre)
    return render_template("index.html", mot_secret=mot_secret, lettres_saisies=lettres_saisies)

if __name__ == "__main__":
    app.run(debug=True)
