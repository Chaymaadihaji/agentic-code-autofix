import json
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Données de jeu
jeu = {
    "vies": 3,
    "score": 0,
    "niveau": 1,
    "monde": 1,
    "piece": 0,
    "ennemi": 0
}

# Données niveaux
niveaux = [
    {
        "plateforme": [[1, 1], [1, 2], [1, 3]],
        "ennemi": {"x": 1, "y": 1},
        "piece": {"x": 2, "y": 2}
    }
]

# Fonction pour générer un ennemi
def generer_ennemi():
    return {"x": random.randint(1, 10), "y": random.randint(1, 10)}

# Fonction pour générer une pièce
def generer_piece():
    return {"x": random.randint(1, 10), "y": random.randint(1, 10)}

# Route pour afficher le jeu
@app.route("/")
def jeu_route():
    return render_template("jeu.html", jeu=jeu, niveaux=niveaux)

# Route pour gérer les actions du joueur
@app.route("/action", methods=["POST"])
def action_route():
    donnees = request.json
    if donnees["action"] == "deplacer":
        # Déplacer le joueur
        jeu["vies"] -= 1
    elif donnees["action"] == "collecter_piece":
        # Collecter une pièce
        jeu["piece"] += 1
    elif donnees["action"] == "tué_ennemi":
        # Tuer un ennemi
        jeu["ennemi"] -= 1
    return jsonify(jeu)

# Route pour gérer les niveaux
@app.route("/niveau", methods=["POST"])
def niveau_route():
    donnees = request.json
    if donnees["action"] == "suivant":
        # Passer au niveau suivant
        jeu["niveau"] += 1
        jeu["monde"] += 1
    return jsonify(jeu)

# Route pour gérer le score
@app.route("/score", methods=["POST"])
def score_route():
    donnees = request.json
    if donnees["action"] == "augmenter":
        # Augmenter le score
        jeu["score"] += 100
    return jsonify(jeu)

# Route pour gérer le boss
@app.route("/boss", methods=["POST"])
def boss_route():
    donnees = request.json
    if donnees["action"] == "defait":
        # Défaire le boss
        jeu["vies"] += 1
    return jsonify(jeu)

if __name__ == "__main__":
    app.run(debug=True)
