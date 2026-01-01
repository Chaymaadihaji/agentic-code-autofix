# config.py
import random

class Config:
    MOTS = ["python", "jeu", "programmation", "langage", "development"]
    MAX_TENTATIVES = 6
    SCORE_MIN = 0
    SCORE_MAX = 100

class JeuPendu:
    def __init__(self, mot=random.choice(Config.MOTS)):
        self.mot = mot
        self.tentatives = 0
        self.score = Config.SCORE_MIN

    def verifier_tentative(self, lettre):
        if lettre in self.mot:
            return True
        else:
            self.tentatives += 1
            return False

    def verifier_fin_jeu(self):
        if self.tentatives == Config.MAX_TENTATIVES:
            return True
        elif "_" not in self.mot:
            return True
        else:
            return False

    def afficher_mot(self):
        return "".join([lettre if lettre != "_" else "_" for lettre in self.mot])

    def afficher_score(self):
        return self.score

    def augmenter_score(self):
        self.score += 10

    def reset_score(self):
        self.score = Config.SCORE_MIN

    def afficher_tentatives(self):
        return self.tentatives

    def verifier_score(self):
        if self.score >= Config.SCORE_MAX:
            return True
        else:
            return False

    def afficher_jeu(self):
        print(f"Mot: {self.afficher_mot()}")
        print(f"Tentatives restantes: {Config.MAX_TENTATIVES - self.tentatives}")
        print(f"Score: {self.score}")
