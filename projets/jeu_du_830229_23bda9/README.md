from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Liste de mots à choisir
mots = ["apple", "banana", "cherry", "date", "elderberry"]

# Fonction pour générer un mot au hasard
def generer_mot():
    return random.choice(mots)

# Fonction pour afficher le pendu
def afficher_pendu(mot, lettres_saisies):
    pendu = ["_"] * len(mot)
    for lettre in lettres_saisies:
        for i, l in enumerate(mot):
            if l == lettre:
                pendu[i] = lettre
    return " ".join(pendu)

# Fonction pour vérifier si le mot a été deviné
def mot_devine(mot, lettres_saisies):
    return all([l in lettres_saisies for l in mot])

# Fonction pour gérer le jeu
def jouer():
    mot = generer_mot()
    lettres_saisies = []
    essais = 6
    while essais > 0 and not mot_devine(mot, lettres_saisies):
        lettres = request.form["lettres"]
        lettres_saisies += [l for l in lettres if l not in lettres_saisies]
        essais -= 1
    return mot, lettres_saisies, essais

# Route pour afficher la page de jeu
@app.route("/")
def jeu():
    return render_template("jeu.html")

# Route pour gérer le jeu
@app.route("/jouer", methods=["POST"])
def jouer_jeu():
    mot, lettres_saisies, essais = jouer()
    return render_template("jeu.html", mot=mot, lettres_saisies=lettres_saisies, essais=essais)

# Lancement du serveur
if __name__ == "__main__":
    app.run(debug=True)
