import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

# Liste de mots pour le jeu
mots = ["apple", "banana", "cherry", "date", "elderberry"]

# Fichier de données pour le score/niveau
donnees_score = {"score": 0, "niveau": 1}

# Fichier de données pour le mot à deviner
donnees_mot = {"mot": random.choice(mots), "tentatives": 0, "lettres_proposees": []}

# Fonction pour vérifier si une lettre est dans le mot
def est_dans_mot(lettre):
    return lettre in donnees_mot["mot"]

# Fonction pour afficher le tableau de jeu
def afficher_tableau():
    tableau = ""
    for lettre in donnees_mot["mot"]:
        if lettre in donnees_mot["lettres_proposees"]:
            tableau += f"<span style='color: green'>{lettre}</span> "
        else:
            tableau += f"<span style='color: red'>{lettre}</span> "
    return tableau

# Fonction pour afficher le score
def afficher_score():
    return donnees_score["score"]

# Fonction pour afficher le niveau
def afficher_niveau():
    return donnees_score["niveau"]

# Route pour afficher le formulaire de jeu
@app.route("/")
def jeu():
    return render_template("jeu.html", tableau=afficher_tableau(), score=afficher_score(), niveau=afficher_niveau())

# Route pour traiter la saisie de la lettre
@app.route("/traiter", methods=["POST"])
def traiter():
    lettre = request.form["lettre"]
    donnees_mot["tentatives"] += 1
    if est_dans_mot(lettre):
        donnees_score["score"] += 1
        donnees_mot["lettres_proposees"].append(lettre)
    else:
        donnees_score["niveau"] += 1
    return render_template("jeu.html", tableau=afficher_tableau(), score=afficher_score(), niveau=afficher_niveau())

# Route pour afficher le score final
@app.route("/fin")
def fin():
    return render_template("fin.html", score=donnees_score["score"])

if __name__ == "__main__":
    app.run(debug=True)
