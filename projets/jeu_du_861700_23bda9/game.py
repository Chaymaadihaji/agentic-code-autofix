import random
from flask import Flask, render_template

app = Flask(__name__)

# Fichier de mots au hasard
mots = ['apple', 'banana', 'cherry', 'date', 'elderberry']

# Nombre de tentatives
tentatives = 0

# État du jeu (mot à deviner, lettres déjà trouvées, lettres incorrectes)
etat_jeu = {
    'mot': '',
    'lettres_trouvees': [],
    'lettres_incorectes': []
}

@app.route('/', methods=['GET', 'POST'])
def jeu():
    global tentatives, etat_jeu

    # Génération d'un mot au hasard
    mot = random.choice(mots)
    etat_jeu['mot'] = mot

    # Initialisation du nombre de tentatives
    tentatives = 4

    # Initialisation de l'état du jeu
    etat_jeu['lettres_trouvees'] = []
    etat_jeu['lettres_incorectes'] = []

    if request.method == 'POST':
        # Récupération de la lettre entrée
        lettre = request.form['lettre']

        # Vérification si la lettre est dans le mot
        if lettre in mot:
            # Ajout de la lettre aux lettres trouvées
            etat_jeu['lettres_trouvees'].append(lettre)
        else:
            # Ajout de la lettre aux lettres incorrectes
            etat_jeu['lettres_incorectes'].append(lettre)
            # Décrément du nombre de tentatives
            tentatives -= 1

        # Vérification si le mot est complètement trouvé
        if all([lettre in etat_jeu['lettres_trouvees'] for lettre in mot]):
            return render_template('gagne.html')
        elif tentatives == 0:
            return render_template('perdu.html')

    return render_template('jeu.html')

if __name__ == "__main__":
    app.run(debug=True)
