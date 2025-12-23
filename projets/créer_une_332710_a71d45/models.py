# models.py
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Données en mémoire
historique = []
calculs = {}

# Fonction pour calculer l'expression
def calcul(expression):
    try:
        return eval(expression)
    except Exception as e:
        return str(e)

# Fonction pour effacer l'historique
def effacer_historique():
    global historique
    historique = []

# Route pour afficher la page principale
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route pour traiter les calculs
@app.route('/calcul', methods=['POST'])
def traitement_calcul():
    global calculs
    expression = request.form['expression']
    calcul = calcul(expression)
    calculs[expression] = calcul
    historique.append(expression)
    if len(historique) > 10:
        historique.pop(0)
    return jsonify({'calcul': calcul, 'historique': historique})

# Route pour afficher l'historique
@app.route('/historique', methods=['GET'])
def afficher_historique():
    global historique
    return jsonify({'historique': historique})

# Route pour effacer l'historique
@app.route('/effacer', methods=['GET'])
def effacer():
    global historique
    effacer_historique()
    return jsonify({'message': 'Historique effacé'})

if __name__ == "__main__":
    app.run(debug=True)
