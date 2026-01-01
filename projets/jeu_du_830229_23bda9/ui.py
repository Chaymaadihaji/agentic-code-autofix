from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Mots à deviner
mots = ["chien", "chat", "oiseau", "renard", "singe"]

# État du jeu
etat_jeu = {
    "mot": "",
    "lettres": [],
    "essais": 6,
    "score": 0
}

# Fonction pour générer le mot au hasard
def generer_mot_aleatoire():
    return random.choice(mots)

# Fonction pour afficher le pendu
def afficher_pendu(lettres):
    pendu = ""
    for lettre in etat_jeu["mot"]:
        if lettre in lettres:
            pendu += lettre + " "
        else:
            pendu += "_ "
    return pendu

# Fonction pour vérifier si le mot a été deviné
def est_devine(mot, lettres):
    return all(char in lettres for char in mot)

# Route pour afficher la page de jeu
@app.route("/")
def jeu():
    global etat_jeu
    etat_jeu["mot"] = generer_mot_aleatoire()
    etat_jeu["lettres"] = []
    etat_jeu["essais"] = 6
    etat_jeu["score"] = 0
    return render_template("jeu.html", pendu=afficher_pendu(etat_jeu["lettres"]))

# Route pour traiter la saisie de lettres
@app.route("/saisie", methods=["POST"])
def saisie():
    global etat_jeu
    lettre = request.form["lettre"]
    if lettre in etat_jeu["lettres"]:
        return render_template("erreur.html", message="Vous avez déjà saisi cette lettre !")
    etat_jeu["lettres"].append(lettre)
    pendu = afficher_pendu(etat_jeu["lettres"])
    if est_devine(etat_jeu["mot"], "".join(etat_jeu["lettres"])):
        etat_jeu["score"] += 1
        return render_template("gagné.html", message="Vous avez gagné !")
    elif etat_jeu["essais"] == 0:
        return render_template("perdu.html", message="Vous avez perdu !")
    else:
        etat_jeu["essais"] -= 1
        return render_template("jeu.html", pendu=pendu, essais=etat_jeu["essais"])

# Route pour afficher la page de fin de jeu
@app.route("/fin")
def fin():
    return render_template("fin.html", score=etat_jeu["score"])

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
