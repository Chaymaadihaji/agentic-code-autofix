import random
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Fichier contenant les mots
mots = "mots.json"

# Fonction pour charger les mots du fichier
def charger_mots():
    with open(mots, "r") as fichier:
        return json.load(fichier)

# Fonction pour générer un mot au hasard
def generer_mot():
    return random.choice(charger_mots())

# Fonction pour afficher le mot avec les lettres masquées
def afficher_mot(mot, lettres_utilisees):
    return "".join([lettre if lettre in lettres_utilisees else "_" for lettre in mot])

# Fonction pour compter le nombre d'essais
def compter_essais(lettres_utilisees, mot):
    return len([lettre for lettre in mot if lettre not in lettres_utilisees])

# Fonction pour vérifier si le mot est trouvé
def mot_trouve(lettres_utilisees, mot):
    return all([lettre in lettres_utilisees for lettre in mot])

# Fonction pour jouer au jeu
def jouer():
    mot = generer_mot()
    lettres_utilisees = set()
    essais = 0
    while essais < 6 and not mot_trouve(lettres_utilisees, mot):
        lettres = request.form.get("lettres")
        if not lettres:
            return jsonify({"erreur": "Vous devez saisir au moins une lettre"}), 400
        for lettre in lettres:
            if lettre in lettres_utilisees:
                return jsonify({"erreur": "Vous avez déjà utilisé cette lettre"}), 400
            lettres_utilisees.add(lettre)
            if lettre not in mot:
                essais += 1
        resultats = {
            "mot": afficher_mot(mot, lettres_utilisees),
            "essais": essais,
            "lettres_utilisees": sorted(list(lettres_utilisees))
        }
        return jsonify(resultats), 200
    if mot_trouve(lettres_utilisees, mot):
        return jsonify({"message": "Félicitations, vous avez trouvé le mot!"}), 200
    return jsonify({"message": "Désolé, vous avez perdu!"}), 200

# Route pour jouer au jeu
@app.route("/jouer", methods=["POST"])
def jouer_route():
    return jouer()

# Route pour afficher la page d'accueil
@app.route("/")
def accueil():
    return render_template("accueil.html")

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
