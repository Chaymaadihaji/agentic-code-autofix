# main.py

import json
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Chemin d'accès aux fichiers
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fonction de validation des caractères Unicode
def valide_caractere_unicode(char):
    return ord(char) >= 0 and ord(char) <= 0x10FFFF

# Fonction de validation des noms de variables avec accents
def valide_nom_variable(nom):
    return any(c.isalnum() or c in '_-' for c in nom)

# Fonction de gestion des caractères Unicode
@app.route('/unicode', methods=['POST'])
def gestion_unicode():
    data = request.get_json()
    caracteres = data['caracteres']
    if all(valide_caractere_unicode(char) for char in caracteres):
        return json.dumps({'resultat': 'ok'})
    else:
        return json.dumps({'resultat': 'erreur'}), 400

# Fonction de gestion des noms de variables avec accents
@app.route('/nom_variable', methods=['POST'])
def gestion_nom_variable():
    data = request.get_json()
    nom = data['nom']
    if valide_nom_variable(nom):
        return json.dumps({'resultat': 'ok'})
    else:
        return json.dumps({'resultat': 'erreur'}), 400

# Route d'index
@app.route('/')
def index():
    return render_template('index.html')

# Route de formulaire
@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        nom = request.form['nom']
        caracteres = request.form['caracteres']
        return render_template('resultat.html', nom=nom, caracteres=caracteres)
    else:
        return render_template('formulaire.html')

if __name__ == "__main__":
    app.run(debug=True)
