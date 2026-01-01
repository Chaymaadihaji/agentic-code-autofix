python
import random
import time

# Liste de mots pour le jeu
mots = ["python", "jeu", "pendu", "code", "developpement"]

def generer_mot_au_hasard():
    """Renvoie un mot au hasard de la liste des mots"""
    return random.choice(mots)

def afficher_mot_masque(mot):
    """Affiche le mot masqué avec des tirets pour les lettres non trouvées"""
    return ["_"] * len(mot)

def verifier_lettre(lettre, mot, tentatives):
    """Vérifie si la lettre est dans le mot et met à jour le mot masqué"""
    mot_masque = afficher_mot_masque(mot)
    if lettre in mot:
        for i in range(len(mot)):
            if mot[i] == lettre:
                mot_masque[i] = lettre
    else:
        tentatives -= 1
        print(f"Erreur ! Tentatives restantes : {tentatives}")
    return mot_masque, tentatives

def jouer():
    """Démarre le jeu du pendu"""
    mot = generer_mot_au_hasard()
    mot_masque = afficher_mot_masque(mot)
    tentatives = 10
    print("Bienvenue dans le jeu du pendu !")
    while tentatives > 0 and "_" in mot_masque:
        print(" ".join(mot_masque))
        lettre = input("Entrez une lettre : ").lower()
        if len(lettre) != 1:
            print("Erreur ! Veuillez entrer une lettre.")
            continue
        if lettre in mot_masque:
            print("Erreur ! Cette lettre a déjà été trouvée.")
            continue
        mot_masque, tentatives = verifier_lettre(lettre, mot, tentatives)
        time.sleep(1)  # Pause de 1 seconde
    if "_" not in mot_masque:
        print("Félicitations ! Vous avez trouvé le mot : " + mot)
    else:
        print("Désolé ! Le mot était " + mot)

if __name__ == "__main__":
    jouer()
