# config.py

import random

class Config:
    MOTS = [
        "chien",
        "chat",
        "oiseau",
        "fleur",
        "arbre",
        "eau",
        "feu",
        "terre"
    ]

    MAX_ERREURS = 6
    SCORE_BASE = 100

    def mot_au_hasard(self):
        return random.choice(self.MOTS)

    def calcul_score(self, erreurs, niveau):
        return self.SCORE_BASE // (erreurs + 1) * niveau

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.score = 0
        self.erreurs = 0
        self.niveau = 1

    def ajouter_score(self, score):
        self.score += score

    def increre_erreurs(self):
        self.erreurs += 1

    def passer_niveau(self):
        self.niveau += 1

    def reset(self):
        self.score = 0
        self.erreurs = 0
        self.niveau = 1

def config():
    return Config()

def joueur(nom):
    return Joueur(nom)

if __name__ == "__main__":
    config()
