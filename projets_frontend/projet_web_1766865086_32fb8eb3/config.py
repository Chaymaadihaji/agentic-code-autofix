# config.py

import os

class Config:
    DEBUG = True
    SECRET_KEY = os.urandom(16).hex()

    # Joueurs
    JOUEURS = []

    # Ennemis
    ENNEMIS = [
        {"id": 1, "nom": "ennemi1", "vitesse": 2},
        {"id": 2, "nom": "ennemi2", "vitesse": 3}
    ]

    # Pièces à collectionner
    PIECES = [
        {"id": 1, "nom": "piece1", "valeur": 10},
        {"id": 2, "nom": "piece2", "valeur": 20}
    ]

    # Niveaux
    NIVEAUX = [
        {"id": 1, "nom": "niveau1", "plateformes": [{"id": 1, "x": 10, "y": 10}, {"id": 2, "x": 20, "y": 20}]},
        {"id": 2, "nom": "niveau2", "plateformes": [{"id": 3, "x": 30, "y": 30}, {"id": 4, "x": 40, "y": 40}]}
    ]

    # Boss
    BOSS = {"id": 1, "nom": "boss", "vitesse": 5}

    # Système de vies
    VIES = 5

    # Score
    SCORE = 0

    # Niveau actuel
    NIVEAU_ACTUEL = 1

    # État du jeu
    ÉTAT_DU_JEU = "en_cours"

# Pour lancer l'application
if __name__ == "__main__":
    from app import application
    application.run(debug=Config.DEBUG)
