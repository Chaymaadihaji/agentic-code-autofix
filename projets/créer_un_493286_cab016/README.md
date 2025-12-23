from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)

class Scores:
    def __init__(self):
        self.vos_scores = 0
        self.ordinateur_scores = 0

class Partie:
    def __init__(self, votre_choix, ordinateur_choix, resultat):
        self.votre_choix = votre_choix
        self.ordinateur_choix = ordinateur_choix
        self.resultat = resultat

scores = Scores()
historique = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form['option']
        choix_ordinateur = random.choice(['pierre', 'papier', 'ciseaux'])
        if option == choix_ordinateur:
            scores.vos_scores += 1
            scores.ordinateur_scores += 1
            resultat = 'Egalité'
        elif (option == 'pierre' and choix_ordinateur == 'ciseaux') or (option == 'papier' and choix_ordinateur == 'pierre') or (option == 'ciseaux' and choix_ordinateur == 'papier'):
            scores.vos_scores += 1
            resultat = 'Vous gagnez'
        else:
            scores.ordinateur_scores += 1
            resultat = 'Ordinateur gagne'
        partie = Partie(option, choix_ordinateur, resultat)
        historique.append(partie)
    return render_template('index.html', scores=scores, historique=historique)

if __name__ == '__main__':
    app.run(debug=True)
