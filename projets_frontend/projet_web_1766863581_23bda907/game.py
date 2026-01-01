from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Liste de mots à choisir au hasard
mots = ['piano', 'guitare', 'batterie', 'basse', 'clavier']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jeu', methods=['GET', 'POST'])
def jeu():
    # Init du jeu
    mot = random.choice(mots)
    lettres = ['_'] * len(mot)
    essais = 0

    # Si formulaire envoyé
    if request.method == 'POST':
        lettre = request.form['lettre']
        if lettre in mot:
            # Recherche la position de la lettre dans le mot
            for i in range(len(mot)):
                if mot[i] == lettre:
                    lettres[i] = lettre
        else:
            essais += 1

    return render_template('jeu.html', mot=mot, lettres=lettres, essais=essais)

if __name__ == "__main__":
    app.run(debug=True)
