import random
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Fichier de données pour les mots au hasard
mots_json = "mots.json"

# Fonction pour charger les mots au hasard
def charger_mots():
    with open(mots_json, "r") as fichier:
        return json.load(fichier)

# Fonction pour générer un mot au hasard
def mot_au_hasard():
    mots = charger_mots()
    return random.choice(mots)

# Fonction pour compter le nombre d'essais
def compter_essais(lettres, mot):
    essais = 0
    for lettre in mot:
        if lettre not in lettres:
            essais += 1
    return essais

# Fonction pour afficher la lettre choisie
def afficher_lettres(lettres, mot):
    affiche = ""
    for lettre in mot:
        if lettre in lettres:
            affiche += lettre + " "
        else:
            affiche += "_ "
    return affiche

# Fonction pour gérer le jeu
def jouer():
    mot = mot_au_hasard()
    lettres = []
    essais = 6
    while essais > 0 and "_" in afficher_lettres(lettres, mot):
        lettre = input("Entrer une lettre : ")
        if lettre in lettres:
            print("Vous avez déjà entré cette lettre.")
        elif lettre in mot:
            print("Bonne lettre !")
            lettres.append(lettre)
        else:
            print("Mauvaise lettre.")
            essais -= 1
            lettres.append(lettre)
        print("Essais restants : ", essais)
        print(afficher_lettres(lettres, mot))
    if essais > 0:
        print("Vous avez gagné ! Le mot était : ", mot)
    else:
        print("Vous avez perdu. Le mot était : ", mot)

# Fonction pour afficher l'interface Web
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mot = mot_au_hasard()
        lettres = []
        essais = 6
        affiche = ""
        for lettre in mot:
            if lettre in lettres:
                affiche += lettre + " "
            else:
                affiche += "_ "
        return render_template("index.html", mot=mot, lettres=lettres, essais=essais, affiche=affiche)
    return render_template("index.html")

# Fonction pour lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
