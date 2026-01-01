# game.py

import random
import json

# Fichier JSON contenant les mots
MOTS_FICHIER = 'mots.json'

class JeuDuPendu:
    def __init__(self):
        self.mots = self.lire_mots_json()
        self.mot_a_deviner = random.choice(self.mots)
        self.lettres_utilisees = []
        self.essais = 6
        self.score = 0

    def lire_mots_json(self):
        with open(MOTS_FICHIER, 'r') as f:
            return json.load(f)

    def generer_mot_aleatoire(self):
        return random.choice(self.mots)

    def afficher_pendu(self):
        print(' _ ' * self.essais)

    def saisir_lettre(self):
        while True:
            lettre = input('Saisir une lettre : ').lower()
            if len(lettre) == 1 and lettre.isalpha():
                return lettre
            print('Saisie incorrecte. Veuillez saisir une lettre.')

    def jouer(self):
        print(f"Score : {self.score}")
        print("Mot à deviner : _ " * len(self.mot_a_deviner))
        while self.essais > 0:
            lettre = self.saisir_lettre()
            if lettre in self.mot_a_deviner:
                print(f"{lettre} est bien dans le mot.")
            else:
                self.essais -= 1
                print(f"{lettre} n'est pas dans le mot. Essais restants : {self.essais}")
            self.lettres_utilisees.append(lettre)
            print("Lettres utilisées : ", ' '.join(self.lettres_utilisees))
        if self.essais == 0:
            print(f"Game over ! Le mot était {self.mot_a_deviner}.")
        else:
            print("Félicitations ! Vous avez gagné !")

    def lancer_jeu(self):
        print("Bienvenue dans le jeu du pendu !")
        self.jouer()
        self.score += 1
        self.mot_a_deviner = self.generer_mot_aleatoire()

def main():
    jeu = JeuDuPendu()
    while True:
        jeu.lancer_jeu()

if __name__ == "__main__":
    main()
