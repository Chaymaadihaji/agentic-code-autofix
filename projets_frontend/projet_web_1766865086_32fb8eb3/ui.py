# ui.py

import json
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Jeu
class Jeu:
    def __init__(self):
        self.vies = 3
        self.score = 0
        self.niveau = 1
        self.monde = 1
        self.pièces = 0
        self.ennemis = []
        self.plateformes = []
        self.boss = False

    def bouger_ennemis(self):
        for ennemi in self.ennemis:
            ennemi['x'] += random.randint(-1, 1)

    def bouger_plateformes(self):
        for plateforme in self.plateformes:
            plateforme['y'] += random.randint(-1, 1)

    def gagner_vie(self):
        self.vies += 1

    def perdre_vie(self):
        self.vies -= 1

    def collecter_pièce(self):
        self.pièces += 1

    def passer_niveau(self):
        self.niveau += 1
        self.monde += 1
        self.boss = False

    def affronter_boss(self):
        self.boss = True

# Données
jeu = Jeu()

# Fonctions
def charger_niveau(niveau):
    with open(f'niveau{niveau}.json', 'r') as f:
        return json.load(f)

def sauvegarder_jeu():
    with open('jeu.json', 'w') as f:
        json.dump({
            'vies': jeu.vies,
            'score': jeu.score,
            'niveau': jeu.niveau,
            'monde': jeu.monde,
            'pièces': jeu.pièces,
            'ennemis': jeu.ennemis,
            'plateformes': jeu.plateformes,
            'boss': jeu.boss
        }, f)

def charger_jeu():
    try:
        with open('jeu.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'vies': 3,
            'score': 0,
            'niveau': 1,
            'monde': 1,
            'pièces': 0,
            'ennemis': [],
            'plateformes': [],
            'boss': False
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html', jeu=charger_jeu())

@app.route('/niveau/<int:niveau>')
def niveau(niveau):
    jeu = charger_jeu()
    jeu.niveau = niveau
    jeu.ennemis = charger_niveau(niveau)['ennemis']
    jeu.plateformes = charger_niveau(niveau)['plateformes']
    jeu.boss = charger_niveau(niveau)['boss']
    sauvegarder_jeu()
    return render_template('niveau.html', jeu=jeu)

@app.route('/collecter', methods=['POST'])
def collecter():
    jeu = charger_jeu()
    jeu.collecter_pièce()
    sauvegarder_jeu()
    return jsonify({'message': 'Pièce collectée'})

@app.route('/vies', methods=['POST'])
def vies():
    jeu = charger_jeu()
    jeu.gagner_vie()
    sauvegarder_jeu()
    return jsonify({'message': 'Vie gagnée'})

@app.route('/perdre', methods=['POST'])
def perdre():
    jeu = charger_jeu()
    jeu.perdre_vie()
    sauvegarder_jeu()
    return jsonify({'message': 'Vie perdue'})

@app.route('/niveau_suivant', methods=['POST'])
def niveau_suivant():
    jeu = charger_jeu()
    jeu.passer_niveau()
    sauvegarder_jeu()
    return jsonify({'message': 'Niveau suivant'})

@app.route('/affronter_boss', methods=['POST'])
def affronter_boss():
    jeu = charger_jeu()
    jeu.affronter_boss()
    sauvegarder_jeu()
    return jsonify({'message': 'Boss affronté'})

if __name__ == "__main__":
    app.run(debug=True)
