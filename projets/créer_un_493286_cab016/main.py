# main.py

import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Données de jeu
scores = {"joueur": 0, "ordinateur": 0}
historique = []
règles = {"pierre": "feuille", "papier": "ciseaux", "ciseaux": "pierre"}

# Chargement des données de jeu depuis un fichier JSON
with open("scores.json", "r") as f:
    scores = json.load(f)

# Fonction de jeu de pierre-papier-ciseaux
def jouer():
    joueur = request.form["joueur"]
    ordinateur = random.choice(["pierre", "papier", "ciseaux"])
    print("Joueur:", joueur)
    print("Ordinateur:", ordinateur)
    
    # Gestion des règles
    if joueur == ordinateur:
        print("Egalité")
    elif (joueur == "pierre" and ordinateur == "ciseaux") or (joueur == "papier" and ordinateur == "pierre") or (joueur == "ciseaux" and ordinateur == "papier"):
        print("Joueur gagne")
        scores["joueur"] += 1
    else:
        print("Ordinateur gagne")
        scores["ordinateur"] += 1
    
    # Ajout à l'historique
    historique.append({"joueur": joueur, "ordinateur": ordinateur, "resultat": scores})
    
    # Sauvegarde des données de jeu
    with open("scores.json", "w") as f:
        json.dump(scores, f)

# Route pour le formulaire de jeu
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        jouer()
    return render_template("index.html", scores=scores, historique=historique)

# Route pour afficher les scores
@app.route("/scores")
def scores():
    return render_template("scores.html", scores=scores)

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
