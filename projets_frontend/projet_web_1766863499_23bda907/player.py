import random
import json

# Fichier de données
with open('words.json') as f:
    mots = json.load(f)

# Génération d'un mot au hasard
def choix_mot():
    return random.choice(list(mots.keys()))

# Initialisation du jeu
def init_jeu():
    mot = choix_mot()
    lettres = ['_'] * len(mot)
    essais = 6
    return mot, lettres, essais

# Saisie de lettre par l'utilisateur
def saisie_lettre(lettres, essais):
    lettre = input("Saisir une lettre : ")
    if len(lettre) != 1:
        print("Saisir une seule lettre.")
        return lettres, essais
    if lettre in lettres:
        print("Vous avez déjà saisi cette lettre.")
        return lettres, essais
    if lettre in mot:
        for i in range(len(mot)):
            if mot[i] == lettre:
                lettres[i] = lettre
    else:
        essais -= 1
        print(f"Essais restants : {essais}")
    return lettres, essais

# Affichage du pendu
def affiche_pendu(lettres, essais):
    print(" ".join(lettres))
    if essais > 0:
        print(f"Essais restants : {essais}")
    else:
        print("Vous avez perdu !")

# Jouer au jeu
def jouer():
    mot, lettres, essais = init_jeu()
    while essais > 0 and "_" in lettres:
        affiche_pendu(lettres, essais)
        lettres, essais = saisie_lettre(lettres, essais)
    affiche_pendu(lettres, essais)
    if "_" not in lettres:
        print("Vous avez gagné !")
    else:
        print(f"Mot : {mot}")

# Lancement du jeu
if __name__ == "__main__":
    jouer()
