# app.py

from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Liste de mots pour le jeu
mots = ["apple", "banana", "cherry", "date", "elderberry"]

# Mot à deviner
mot_a_deviner = random.choice(mots)

# Nombre d'essais
essais = 6

# Liste de lettres déjà tentées
lettres_tentees = []

@app.route("/", methods=["GET", "POST"])
def index():
    global mot_a_deviner
    global essais
    global lettres_tentees

    if request.method == "POST":
        lettre = request.form["lettre"]
        lettres_tentees.append(lettre)

        if lettre in mot_a_deviner:
            # Mise à jour du mot à deviner
            mot_a_deviner = mot_a_deviner.replace(lettre, "")
        else:
            # Réduction du nombre d'essais
            essais -= 1

    return render_template("index.html", mot_a_deviner=mot_a_deviner, essais=essais, lettres_tentees=lettres_tentees)

if __name__ == "__main__":
    app.run(debug=True)
