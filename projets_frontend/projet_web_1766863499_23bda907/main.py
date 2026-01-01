import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Mots à deviner
mots = ['apple', 'banana', 'cherry', 'date', 'elderberry']

# État du jeu
etat_jeu = {
    'mot': random.choice(mots),
    'lettres_proposes': [],
    'lettres_reussies': [],
    'lettres_erreur': [],
    'vies': 6,
    'score': 0
}

# Fonction pour générer le pendu
def generate_pendu(vies):
    if vies == 6:
        return ['O']
    elif vies == 5:
        return ['O', '|']
    elif vies == 4:
        return ['O', '|', '/']
    elif vies == 3:
        return ['O', '|', '/', '\\']
    elif vies == 2:
        return ['O', '|', '/', '\\', '\\']
    elif vies == 1:
        return ['O', '|', '/', '\\', '\\', '/']
    else:
        return ['X', '|', '/', '\\', '\\', '/']

# Route pour afficher le jeu
@app.route('/', methods=['GET', 'POST'])
def jeu():
    global etat_jeu
    if request.method == 'POST':
        lettre = request.form['lettre']
        etat_jeu['lettres_proposes'].append(lettre)
        if len(lettre) != 1 or not lettre.isalpha():
            return render_template('jeu.html', etat_jeu=etat_jeu, pendu=generate_pendu(etat_jeu['vies']), erreurs='Veuillez saisir une lettre.')
        elif lettre in etat_jeu['lettres_reussies'] or lettre in etat_jeu['lettres_erreur']:
            return render_template('jeu.html', etat_jeu=etat_jeu, pendu=generate_pendu(etat_jeu['vies']), erreurs='Veuillez saisir une lettre qui n\'a pas encore été proposée.')
        else:
            if lettre in etat_jeu['mot']:
                etat_jeu['lettres_reussies'].append(lettre)
                if len(etat_jeu['lettres_reussies']) == len(etat_jeu['mot']):
                    etat_jeu['score'] += 10
                    etat_jeu['vies'] = 6
                    return render_template('jeu.html', etat_jeu=etat_jeu, pendu=generate_pendu(etat_jeu['vies']), succes='Félicitations, vous avez gagné!')
            else:
                etat_jeu['lettres_erreur'].append(lettre)
                etat_jeu['vies'] -= 1
                if etat_jeu['vies'] == 0:
                    etat_jeu['score'] -= 10
                    return render_template('jeu.html', etat_jeu=etat_jeu, pendu=generate_pendu(etat_jeu['vies']), erreurs='Désolé, vous avez perdu.')
    return render_template('jeu.html', etat_jeu=etat_jeu, pendu=generate_pendu(etat_jeu['vies']))

if __name__ == "__main__":
    app.run(debug=True)
