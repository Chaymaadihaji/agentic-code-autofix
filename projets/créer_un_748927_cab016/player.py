# player.py

import random
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Gestion des scores
scores = {
    'pierre': 0,
    'papier': 0,
    'ciseaux': 0
}

# Historique des parties
parties = []

# Logique du jeu
def jeu(joueur1, joueur2):
    if joueur1 == joueur2:
        return "Egalité"
    if (joueur1 == 'pierre' and joueur2 == 'ciseaux') or (joueur1 == 'papier' and joueur2 == 'pierre') or (joueur1 == 'ciseaux' and joueur2 == 'papier'):
        return "Joueur 1 gagne"
    else:
        return "Joueur 2 gagne"

# Fonction pour gérer l'interface utilisateur
def interface():
    choix_joueur1 = request.form['choix_joueur1']
    choix_joueur2 = random.choice(['pierre', 'papier', 'ciseaux'])
    resultat = jeu(choix_joueur1, choix_joueur2)
    scores[choix_joueur1] += 1 if resultat == "Joueur 1 gagne" else 0
    parties.append({
        'joueur1': choix_joueur1,
        'joueur2': choix_joueur2,
        'resultat': resultat
    })
    return render_template('index.html', scores=scores, parties=parties)

# Route pour l'interface utilisateur
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return interface()
    return render_template('index.html', scores=scores, parties=parties)

# Route pour afficher les scores et l'historique
@app.route('/scores', methods=['GET'])
def scores_route():
    return render_template('scores.html', scores=scores, parties=parties)

# Route pour afficher l'historique
@app.route('/historique', methods=['GET'])
def historique_route():
    return render_template('historique.html', parties=parties)

# Lancement de l'app
if __name__ == "__main__":
    app.run(debug=True)
