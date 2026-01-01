# ui.py

import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionnaire de mots à deviner
mots_a_deviner = {
    "facile": ["poulet", "fleur", "pain"],
    "moyen": ["ordinateur", "bibliothèque", "champignon"],
    "difficile": ["astronomie", "physique", "chimie"]
}

# État du jeu
etat_jeu = {
    "mot": "",
    "lettres_utilisees": [],
    "essais": 6,
    "score": 0
}

# Fonction pour générer un mot aléatoire
def generer_mot_difficile(niveau):
    return random.choice(mots_a_deviner[niveau])

# Fonction pour vérifier si une lettre est présente dans le mot
def est présente(lettre):
    return lettre in etat_jeu["mot"]

# Fonction pour gérer le jeu
def gérer_jeu():
    global etat_jeu
    mot = generer_mot_difficile("moyen")
    etat_jeu["mot"] = "_" * len(mot)
    etat_jeu["lettres_utilisees"] = []
    etat_jeu["essais"] = 6
    etat_jeu["score"] = 0

# Fonction pour afficher le tableau de jeu
def afficher_tableau():
    tableau = []
    for lettre in etat_jeu["mot"]:
        tableau.append("_")
    return " ".join(tableau)

# Fonction pour afficher les résultats
def afficher_resultats():
    return str(etat_jeu["essais"]) + " essais restants"

# Fonction pour gérer la saisie de lettres
def saisie_lettre(lettre):
    global etat_jeu
    if lettre in etat_jeu["lettres_utilisees"]:
        return False
    etat_jeu["lettres_utilisees"].append(lettre)
    if est présente(lettre):
        for i, m in enumerate(etat_jeu["mot"]):
            if m == lettre:
                etat_jeu["mot"] = etat_jeu["mot"][:i] + lettre + etat_jeu["mot"][i+1:]
    else:
        etat_jeu["essais"] -= 1
    if "_" not in etat_jeu["mot"]:
        etat_jeu["score"] += 1
        gérer_jeu()
    return True

# Route pour afficher le formulaire
@app.route("/")
def formulaire():
    return render_template("formulaire.html", tableau=afficher_tableau(), resultats=afficher_resultats())

# Route pour gérer la saisie de lettres
@app.route("/saisie", methods=["POST"])
def saisie():
    lettre = request.form["lettre"]
    if saisie_lettre(lettre):
        return render_template("formulaire.html", tableau=afficher_tableau(), resultats=afficher_resultats())
    else:
        return render_template("erreur.html", message="Trop d'essais !")

if __name__ == "__main__":
    gérer_jeu()
    app.run(debug=True)
