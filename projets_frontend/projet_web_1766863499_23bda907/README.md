import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Mots à deviner
mots = ["apple", "banana", "cherry", "date", "elderberry"]

# Nombre de segments du pendu
segments = 6

# Lettres saisies
lettres = []

@app.route("/")
def index():
    # Mot au hasard
    mot = random.choice(mots)
    return render_template("index.html", mot=mot, segments=segments, lettres=lettres)

@app.route("/verifier", methods=["POST"])
def verifier():
    global segments, lettres
    lettre = request.form["lettre"]
    lettres.append(lettre)
    if lettre not in mot:
        segments -= 1
    if segments == 0:
        return "Perdu ! Le mot était " + mot
    elif len(lettres) == len(mot):
        return "Gagné ! Le mot était " + mot
    return render_template("index.html", mot=mot, segments=segments, lettres=lettres)

if __name__ == "__main__":
    app.run(debug=True)
