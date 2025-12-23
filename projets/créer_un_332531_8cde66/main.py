# main.py

from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Chargement des citations depuis un fichier JSON
with open('citations.json') as f:
    citations = json.load(f)

# Route principale
@app.route('/')
def index():
    # Génération d'une citation aléatoire
    citation = random.choice(citations['citations'])
    return render_template('index.html', citation=citation)

# Route pour rafraîchir la citation
@app.route('/rafraîchir')
def rafraîchir():
    return render_template('index.html')

# Route pour afficher les citations
@app.route('/citations')
def citations_list():
    return render_template('citations.html', citations=citations['citations'])

# Route pour générer une citation aléatoire en JSON
@app.route('/citation/<int:id>')
def citation_json(id):
    if id < len(citations['citations']):
        return json.dumps({'citation': citations['citations'][id]})
    else:
        return 'Citation non trouvée', 404

# Gestion des erreurs
@app.errorhandler(404)
def page_not_found(e):
    return 'Page non trouvée', 404

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
