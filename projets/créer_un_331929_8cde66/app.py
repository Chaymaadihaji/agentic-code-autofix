from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Chemin vers le fichier JSON contenant les citations
JSON_FILE = 'citations.json'

# Chargement des citations à partir du fichier JSON
with open(JSON_FILE, 'r') as fichier:
    citations = json.load(fichier)

# Fonction de génération d'une citation aléatoire
def get_citation():
    return random.choice(citations)

# Route principale pour afficher une citation
@app.route('/', methods=['GET'])
def index():
    citation = get_citation()
    return render_template('index.html', citation=citation)

# Route pour rafraîchir la citation
@app.route('/rafraîchir', methods=['GET'])
def rafraîchir():
    citation = get_citation()
    return render_template('index.html', citation=citation)

# Route pour afficher les erreurs
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
