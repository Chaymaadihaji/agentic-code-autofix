import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Dossier contenant les mots à deviner
mots = ['apple', 'banana', 'cherry', 'date', 'elderberry']

# Nombre de tentatives pour gagner
tentatives = 6

# État du jeu
etat = {
    'mot': random.choice(mots),
    'lettres_proposes': [],
    'lettres_incorrectes': [],
    'lettres_correctes': [],
    'tentatives': tentatives
}

@app.route('/')
def index():
    global etat
    return render_template('index.html', etat=etat)

@app.route('/proposition', methods=['POST'])
def proposition():
    global etat
    lettre = request.form['lettre']
    if lettre in etat['mot']:
        etat['lettres_correctes'].append(lettre)
    else:
        etat['lettres_incorrectes'].append(lettre)
        etat['tentatives'] -= 1
    return render_template('index.html', etat=etat)

@app.route('/recommencer')
def recommencer():
    global etat
    etat = {
        'mot': random.choice(mots),
        'lettres_proposes': [],
        'lettres_incorrectes': [],
        'lettres_correctes': [],
        'tentatives': tentatives
    }
    return render_template('index.html', etat=etat)

if __name__ == "__main__":
    app.run(debug=True)
