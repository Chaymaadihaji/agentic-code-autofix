# game.py
import random
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Système de scores
scores = {
    "joueur1": {"victoires": 0, "défaites": 0},
    "joueur2": {"victoires": 0, "défaites": 0}
}

# Historique des parties
historique = []

# Fonction de gestion des scores
def maj_scores(joueur, resultat):
    if resultat == "gagné":
        scores[joueur]["victoires"] += 1
    elif resultat == "perdu":
        scores[joueur]["défaites"] += 1

# Fonction de jeu de pierre-papier-ciseaux
def jouer_pierre_papier_ciseaux(joueur1, joueur2):
    options = ["pierre", "papier", "ciseaux"]
    choix_joueur1 = random.choice(options)
    choix_joueur2 = random.choice(options)
    print(f"Joueur 1 : {choix_joueur1}, Joueur 2 : {choix_joueur2}")
    if choix_joueur1 == choix_joueur2:
        return "égal"
    elif (choix_joueur1 == "pierre" and choix_joueur2 == "ciseaux") or \
         (choix_joueur1 == "papier" and choix_joueur2 == "pierre") or \
         (choix_joueur1 == "ciseaux" and choix_joueur2 == "papier"):
        return "gagné"
    else:
        return "perdu"

# Route pour afficher l'écran de jeu
@app.route("/")
def jeu():
    return render_template("jeu.html")

# Route pour jouer la partie
@app.route("/jouer", methods=["POST"])
def jouer():
    joueur1 = request.form["joueur1"]
    joueur2 = request.form["joueur2"]
    resultat = jouer_pierre_papier_ciseaux(joueur1, joueur2)
    maj_scores(joueur1, resultat)
    maj_scores(joueur2, "perdu" if resultat == "gagné" else "gagné")
    historique.append({"joueur1": joueur1, "joueur2": joueur2, "resultat": resultat})
    return jsonify({"resultat": resultat, "scores": scores, "historique": historique})

# Route pour afficher les scores et l'historique
@app.route("/scores")
def scores():
    return render_template("scores.html", scores=scores, historique=historique)

if __name__ == "__main__":
    app.run(debug=True)
