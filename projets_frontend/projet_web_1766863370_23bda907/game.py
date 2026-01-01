import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

# Mots à deviner
mots = ["apple", "banana", "cherry", "date"]

# État du jeu
etat_jeu = {}
etat_jeu["mot"] = random.choice(mots)
etat_jeu["lettres_tries"] = []
etat_jeu["lettres_proposes"] = []
etat_jeu["erreurs"] = 0
etat_jeu["score"] = 0

# Fonction pour générer un mot au hasard
def generer_mot():
    return random.choice(mots)

# Fonction pour afficher le jeu
def afficher_jeu():
    return render_template("jeu.html", etat_jeu=etat_jeu)

# Fonction pour gérer la saisie de lettres
def gérer_saisie_lettre(lettre):
    if lettre in etat_jeu["lettres_tries"]:
        return "Lettre déjà proposée"
    elif lettre in etat_jeu["mot"]:
        etat_jeu["lettres_proposes"].append(lettre)
    else:
        etat_jeu["erreurs"] += 1
        etat_jeu["lettres_tries"].append(lettre)
    return "Lettre proposée"

# Fonction pour gérer la fin du jeu
def gérer_fin_jeu():
    if etat_jeu["erreurs"] >= 6:
        return "Fin de jeu : Perdu"
    elif "_" not in etat_jeu["mot"]:
        etat_jeu["score"] += 10
        return "Fin de jeu : Gagné"
    else:
        return "Continuer le jeu"

# Route pour afficher le jeu
@app.route("/")
def jeu():
    return afficher_jeu()

# Route pour gérer la saisie de lettres
@app.route("/saisie_lettre", methods=["POST"])
def saisie_lettre():
    lettre = request.form["lettre"]
    return gérer_saisie_lettre(lettre)

# Route pour gérer la fin du jeu
@app.route("/fin_jeu", methods=["POST"])
def fin_jeu():
    return gérer_fin_jeu()

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
