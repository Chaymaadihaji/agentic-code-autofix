# config.py

import random

class Config:
    MOTS = ["chien", "chat", "pont", "mère", "père"]
    LIVRES = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
             "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
             "y", "z"]
    MAX_ERREURS = 6

class Jeu:
    def __init__(self):
        self.mot = random.choice(Config.MOTS)
        self.etat = ["_"] * len(self.mot)
        self.erreurs = 0
        self.score = 0

    def verifier(self, lettre):
        if lettre in self.mot:
            for i in range(len(self.mot)):
                if self.mot[i] == lettre:
                    self.etat[i] = lettre
        else:
            self.erreurs += 1

    def afficher(self):
        print(" ".join(self.etat))
        print(f"Erreurs : {self.erreurs}/{Config.MAX_ERREURS}")
        print(f"Score : {self.score}")
