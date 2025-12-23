# ui.py

from flask import Flask, render_template, request
import random
import json

app = Flask(__name__)

# Structure de données pour les scores et historique
scores = {"joueur": 0, "ordinateur": 0}
historique = []

# Chemin du fichier JSON pour les scores et historique
fichier_scores = "scores.json"

# Fonction pour gérer les scores
def sauvegarder_scores():
    with open(fichier_scores, "w") as fichier:
        json.dump(scores, fichier)

def charger_scores():
    try:
        with open(fichier_scores, "r") as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        return {"joueur": 0, "ordinateur": 0}

# Fonction pour jouer au jeu
def jouer():
    choix_user = request.form["choix"]
    choix_ordinateur = random.choice(["pierre", "papier", "ciseaux"])

    if choix_user == choix_ordinateur:
        return "Egalité"
    elif (choix_user == "pierre" and choix_ordinateur == "ciseaux") or \
         (choix_user == "papier" and choix_ordinateur == "pierre") or \
         (choix_user == "ciseaux" and choix_ordinateur == "papier"):
        scores["joueur"] += 1
        return "Gagné"
    else:
        scores["ordinateur"] += 1
        return "Perdu"

# Route pour afficher l'écran de jeu
@app.route("/")
def index():
    return render_template("index.html")

# Route pour jouer au jeu
@app.route("/jouer", methods=["POST"])
def jouer_route():
    resultat = jouer()
    historique.append({"user": request.form["choix"], "ordinateur": random.choice(["pierre", "papier", "ciseaux"]), "resultat": resultat})
    sauvegarder_scores()
    return render_template("resultat.html", resultat=resultat, historique=historique)

# Route pour afficher l'historique des parties
@app.route("/historique")
def historique_route():
    global historique
    historique = charger_scores()["historique"]
    return render_template("historique.html", historique=historique)

if __name__ == "__main__":
    app.run(debug=True)
