# config.py
import json

class Config:
    JSON_FILE = 'parties.json'

    def __init__(self):
        self.parties = self.load_parties()

    def load_parties(self):
        try:
            with open(self.JSON_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_parties(self):
        with open(self.JSON_FILE, 'w') as f:
            json.dump(self.parties, f)

    def ajouter_partie(self, gagnant, perdant):
        self.parties.append({
            'gagnant': gagnant,
            'perdant': perdant
        })
        self.save_parties()

    def get_historique(self):
        return self.parties

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.score = 0

class Partie:
    def __init__(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.resultat = None

    def jouer(self):
        import random
        choix1 = random.choice(['pierre', 'papier', 'ciseaux'])
        choix2 = random.choice(['pierre', 'papier', 'ciseaux'])
        if (choix1 == 'pierre' and choix2 == 'ciseaux') or (choix1 == 'papier' and choix2 == 'pierre') or (choix1 == 'ciseaux' and choix2 == 'papier'):
            self.resultat = self.joueur1.nom
        elif choix1 == choix2:
            self.resultat = 'égalité'
        else:
            self.resultat = self.joueur2.nom

        if self.resultat != 'égalité':
            self.gagnant.score += 1
            self.perdant.score -= 1

class Application:
    def __init__(self):
        self.config = Config()
        self.joueurs = {
            'joueur1': Joueur('Joueur 1'),
            'joueur2': Joueur('Joueur 2')
        }

    def lancer_partie(self):
        partie = Partie(self.joueurs['joueur1'], self.joueurs['joueur2'])
        partie.jouer()
        self.config.ajouter_partie(partie.resultat, 'inconnu')

    def afficher_historique(self):
        print(self.config.get_historique())

if __name__ == "__main__":
    app = Application()
    while True:
        print("1. Lancer une partie")
        print("2. Afficher l'historique")
        choix = input("Choisissez une option : ")
        if choix == '1':
            app.lancer_partie()
        elif choix == '2':
            app.afficher_historique()
        else:
            print("Option invalide")
