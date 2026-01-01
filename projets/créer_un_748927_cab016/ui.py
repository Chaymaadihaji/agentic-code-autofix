from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Données en mémoire
scores = {
    'jeux_gagnés': 0,
    'jeux_perdus': 0,
    'jeux_nuls': 0
}
historique = []

# Fonction pour jouer un jeu
def jouer_jeu(user, ordi):
    if user == 'pierre' and ordi == 'ciseaux':
        return 'gagné'
    elif user == 'pierre' and ordi == 'papier':
        return 'perdu'
    elif user == 'pierre' and ordi == 'pierre':
        return 'nul'
    elif user == 'papier' and ordi == 'pierre':
        return 'gagné'
    elif user == 'papier' and ordi == 'ciseaux':
        return 'perdu'
    elif user == 'papier' and ordi == 'papier':
        return 'nul'
    elif user == 'ciseaux' and ordi == 'papier':
        return 'gagné'
    elif user == 'ciseaux' and ordi == 'pierre':
        return 'perdu'
    elif user == 'ciseaux' and ordi == 'ciseaux':
        return 'nul'

# Fonction pour gérer les scores
def gérer_scores(resultat):
    global scores
    if resultat == 'gagné':
        scores['jeux_gagnés'] += 1
    elif resultat == 'perdu':
        scores['jeux_perdus'] += 1
    elif resultat == 'nul':
        scores['jeux_nuls'] += 1
    historique.append(resultat)

# Fonction pour générer une carte aléatoire
def generer_ordi():
    retour = random.choice(['pierre', 'papier', 'ciseaux'])
    return retour

# Route pour jouer un jeu
@app.route('/jouer', methods=['POST'])
def jouer():
    user = request.form['user']
    ordi = generer_ordi()
    resultat = jouer_jeu(user, ordi)
    gérer_scores(resultat)
    return 'Vous avez joué ' + user + ' contre ' + ordi + '. Le résultat est ' + resultat + '.'

# Route pour afficher les scores
@app.route('/scores')
def scores():
    return render_template('scores.html', scores=scores)

# Route pour afficher l'historique
@app.route('/historique')
def historique():
    return render_template('historique.html', historique=historique)

# Route pour afficher l'écran de jeu
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
