from flask import Flask, render_template, request, make_response
from collections import deque

app = Flask(__name__)

# Historique des calculs
history = deque(maxlen=10)

# Fonction pour calculer l'expression
def calculer(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return str(e)

# Fonction pour afficher l'historique
def afficher_historique():
    return '\n'.join(history)

# Fonction pour effacer l'historique
def effacer_historique():
    global history
    history = deque(maxlen=10)

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour le calcul
@app.route('/calcul', methods=['POST'])
def calcul():
    expression = request.form['expression']
    result = calculer(expression)
    history.append(expression + ' = ' + result)
    return render_template('resultat.html', result=result, history=afficher_historique())

# Route pour effacer l'historique
@app.route('/effacer', methods=['POST'])
def effacer():
    effacer_historique()
    return render_template('index.html')

# Route pour afficher l'historique
@app.route('/historique')
def historique():
    return render_template('historique.html', history=afficher_historique())

if __name__ == "__main__":
    app.run(debug=True)
