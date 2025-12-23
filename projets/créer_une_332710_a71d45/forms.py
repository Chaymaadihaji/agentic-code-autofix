# forms.py

from flask import Flask, render_template, request, jsonify
import json
import operator

app = Flask(__name__)

# Historique des calculs
historique = []
MAX_HISTOIRE = 10

# Fonctions de calcul
calculs = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# Fonction pour traiter les calculs
def traitement_calcul(num1, op, num2):
    try:
        return calculs[op](num1, num2)
    except ZeroDivisionError:
        return "Erreur : division par zéro"

# Fonction pour effacer l'historique
def effacer_historique():
    global historique
    historique = []

# Route pour afficher la page de calculatrice
@app.route('/', methods=['GET'])
def calculatrice():
    return render_template('calculatrice.html')

# Route pour traiter les saisies utilisateur
@app.route('/', methods=['POST'])
def traitement saisie():
    num1 = float(request.form['num1'])
    op = request.form['op']
    num2 = float(request.form['num2'])
    resultat = traitement_calcul(num1, op, num2)
    historique.append((num1, op, num2, resultat))
    if len(historique) > MAX_HISTOIRE:
        historique.pop(0)
    return jsonify({'resultat': resultat, 'historique': historique})

# Route pour effacer l'historique
@app.route('/effacer', methods=['GET'])
def effacer():
    effacer_historique()
    return jsonify({'historique': historique})

if __name__ == "__main__":
    app.run(debug=True)
