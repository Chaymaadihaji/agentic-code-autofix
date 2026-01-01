from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Liste de mots pour le jeu
mots = ["apple", "banana", "cherry", "date", "elderberry"]

@app.route("/")
def index():
    mot = random.choice(mots)
    return render_template("index.html", mot=mot, tentatives=6, guessed_letters="")

@app.route("/guess", methods=["POST"])
def guess():
    mot = request.form["mot"]
    lettre = request.form["lettre"]
    tentatives = int(request.form["tentatives"])
    guessed_letters = request.form["guessed_letters"]
    
    if lettre in mot:
        return render_template("index.html", mot=mot, tentatives=tentatives, guessed_letters=guessed_letters + lettre)
    else:
        return render_template("index.html", mot=mot, tentatives=tentatives-1, guessed_letters=guessed_letters + lettre + " (mauvaise)")

if __name__ == "__main__":
    app.run(debug=True)
