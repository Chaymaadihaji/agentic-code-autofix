# player.py

import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Gestion des scores
scores = {
    'joueur1': 0,
    'joueur2': 0
}

# Historique des parties
historique = []

# Fonction pour générer un choix aléatoire
def generer_choix():
    return random.choice(['pierre', 'papier', 'ciseaux'])

# Fonction pour déterminer le gagnant
def determiner_gagnant(choix_joueur1, choix_joueur2):
    if choix_joueur1 == choix_joueur2:
        return 'égalité'
    if (choix_joueur1 == 'pierre' and choix_joueur2 == 'ciseaux') or \
       (choix_joueur1 == 'papier' and choix_joueur2 == 'pierre') or \
       (choix_joueur1 == 'ciseaux' and choix_joueur2 == 'papier'):
        return 'joueur1'
    return 'joueur2'

# Route pour afficher l'écran de jeu
@app.route('/')
def jeu():
    return render_template('jeu.html')

# Route pour traiter le formulaire de jeu
@app.route('/jeu', methods=['POST'])
def traiter_jeu():
    choix_joueur1 = request.form['choix_joueur1']
    choix_joueur2 = generer_choix()
    gagnant = determiner_gagnant(choix_joueur1, choix_joueur2)
    scores[gagnant] += 1
    historique.append({'choix_joueur1': choix_joueur1, 'choix_joueur2': choix_joueur2, 'gagnant': gagnant})
    return render_template('resultat.html', choix_joueur1=choix_joueur1, choix_joueur2=choix_joueur2, gagnant=gagnant)

# Route pour afficher l'historique
@app.route('/historique')
def historique_jeu():
    return render_template('historique.html', historique=historique)

if __name__ == "__main__":
    app.run(debug=True)
