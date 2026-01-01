# player.py

import random
import json
from flask import Flask, request, render_template

app = Flask(__name__)

# Données de jeux
jeux = {
    "facile": {"mots": ["chien", "chat", "oiseau", "fleur"], "score": 0},
    "moyen": {"mots": ["ordinateur", "telephone", "piano", "guitare"], "score": 0},
    "difficile": {"mots": ["astronomie", "physique", "informatique", "mathematiques"], "score": 0}
}

# Fonction pour générer un mot au hasard
def generer_mot_difficulte(niveau):
    return random.choice(jeux[niveau]["mots"])

# Fonction pour afficher le tableau de jeu
def afficher_tableau(lettres_utilisees, mot, essais):
    tableau = []
    for i, lettre in enumerate(mot):
        if lettre in lettres_utilisees:
            tableau.append(lettre)
        else:
            tableau.append("_")
    return tableau

# Fonction pour gérer le jeu
def jouer(niveau):
    mot = generer_mot_difficulte(niveau)
    lettres_utilisees = []
    essais = 6
    score = 0
    while essais > 0 and "_" in afficher_tableau(lettres_utilisees, mot, essais):
        tableau = afficher_tableau(lettres_utilisees, mot, essais)
        print(" ".join(tableau))
        lettre = input("Saisir une lettre : ")
        if lettre in mot:
            lettres_utilisees.append(lettre)
        else:
            essais -= 1
            lettres_utilisees.append(lettre)
        score += 1
    if "_" not in afficher_tableau(lettres_utilisees, mot, essais):
        print("Bravo ! Vous avez trouvé le mot !")
        score += 10
    else:
        print("Désolé, vous avez perdu ! Le mot était : " + mot)
    jeux[niveau]["score"] += score
    return score

# Route pour afficher les données de jeux
@app.route("/donnees", methods=["GET"])
def donnees():
    return json.dumps(jeux)

# Route pour jouer le jeu
@app.route("/jouer", methods=["GET", "POST"])
def jouer_jeu():
    niveau = request.form["niveau"]
    score = jouer(niveau)
    return render_template("resultat.html", score=score)

# Route pour afficher le résultat
@app.route("/resultat", methods=["GET"])
def resultat():
    return render_template("resultat.html")

if __name__ == "__main__":
    app.run(debug=True)
