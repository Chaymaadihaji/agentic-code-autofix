# main.py

from flask import Flask, render_template, request, jsonify
from random import choice
import os

app = Flask(__name__)

# Dictionnaire de mots pour le jeu
mots = {
    "facile": ["papillon", "fleur", "cercle"],
    "moyen": ["ordinateur", "bibliothèque", "harmonie"],
    "difficile": ["phénoménologie", "éphémère", "cathédrale"]
}

# Chemin vers le fichier de scores
chemin_scores = "scores.json"

# Génération du mot au hasard
def generer_mot(niveau):
    if niveau in mots:
        return choice(mots[niveau])
    else:
        return choice(list(mots.values())[0])

# Fonction pour afficher le pendu
def afficher_pendu(mot, lettres_guessées):
    pendu = ""
    for lettre in mot:
        if lettre in lettres_guessées:
            pendu += lettre + " "
        else:
            pendu += "_ "
    return pendu

# Fonction pour sauvegarder les scores
def sauvegarder_scores(nom, score):
    if os.path.exists(chemin_scores):
        with open(chemin_scores, "r") as f:
            scores = json.load(f)
    else:
        scores = {}
    scores[nom] = score
    with open(chemin_scores, "w") as f:
        json.dump(scores, f)

# Fonction pour charger les scores
def charger_scores():
    if os.path.exists(chemin_scores):
        with open(chemin_scores, "r") as f:
            return json.load(f)
    else:
        return {}

# Route pour afficher le formulaire de jeu
@app.route("/", methods=["GET"])
def formulaire_jeu():
    return render_template("formulaire_jeu.html")

# Route pour traiter les lettres guessées
@app.route("/guess", methods=["POST"])
def guess():
    mot = generer_mot(request.form["niveau"])
    lettres_guessées = request.form["lettres_guessées"].split()
    pendu = afficher_pendu(mot, lettres_guessées)
    score = len(mot) - len(pendu.replace("_", ""))
    return jsonify({"mot": mot, "pendu": pendu, "score": score})

# Route pour sauvegarder les scores
@app.route("/sauvegarder_scores", methods=["POST"])
def sauvegarder_scores_route():
    nom = request.form["nom"]
    score = request.form["score"]
    sauvegarder_scores(nom, int(score))
    return jsonify({"message": "Scores sauvegardés avec succès"})

# Route pour charger les scores
@app.route("/charger_scores", methods=["GET"])
def charger_scores_route():
    scores = charger_scores()
    return jsonify(scores)

if __name__ == "__main__":
    app.run(debug=True)
