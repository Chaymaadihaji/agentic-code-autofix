# config.py

import random
import json

# Configuration du jeu
MOTS_PAR_DEFAUT = ["apple", "banana", "cherry"]
NB_LIGNES_TABLEAU = 6

# Chargement des mots au hasard
def charger_mots():
    return random.choice(MOTS_PAR_DEFAUT)

# Charger les données de score
def charger_score():
    try:
        with open('score.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'score': 0, 'niveaux': 1}

# Enregistrer les données de score
def enregistrer_score(score):
    with open('score.json', 'w') as f:
        json.dump(score, f)

# Générer le tableau du pendu
def generer_tableau(mot):
    tableau = ['_'] * len(mot)
    return tableau

# Afficher le pendu
def afficher_pendu(tableau, lettres_utilisees):
    print(' '.join(tableau))
    print(f'Lettres utilisées : {lettres_utilisees}')

# Vérifier si la lettre est dans le mot
def verifier_lettre(mot, lettre, tableau):
    index = [i for i, l in enumerate(mot) if l == lettre]
    for i in index:
        tableau[i] = lettre
    return tableau

# Vérifier si le mot est trouvé
def verifier_mot(mot, tableau):
    return '_' not in tableau

# Saisir la lettre de l'utilisateur
def saisir_lettre():
    lettre = input('Saisir une lettre : ').lower()
    return lettre

# Lancer le jeu
def lancer_jeu():
    mot = charger_mots()
    score = charger_score()
    tableau = generer_tableau(mot)
    lettres_utilisees = ''
    while '_' in tableau and len(lettres_utilisees) < NB_LIGNES_TABLEAU:
        afficher_pendu(tableau, lettres_utilisees)
        lettre = saisir_lettre()
        if lettre in lettres_utilisees:
            print('Lettre déjà utilisée !')
        elif lettre in mot:
            tableau = verifier_lettre(mot, lettre, tableau)
        else:
            lettres_utilisees += lettre
            print('Lettre non trouvée !')
        if '_' not in tableau:
            print('Félicitations, vous avez trouvé le mot !')
            score['score'] += 1
            score['niveaux'] += 1
            enregistrer_score(score)
            return
    print('Désolé, vous avez perdu !')
    score['niveaux'] += 1
    enregistrer_score(score)

# Lancement de l'application
if __name__ == "__main__":
    lancer_jeu()
