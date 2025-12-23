# app.py

import os
from flask import Flask, render_template, request
import json

# Configuration
app = Flask(__name__)
data_file = 'citations.json'

# Chargement des citations
with open(data_file, 'r') as f:
    citations = json.load(f)

# Route principale
@app.route('/')
def index():
    citation = random_citation(citations)
    return render_template('index.html', citation=citation)

# Route pour générer une nouvelle citation
@app.route('/nouvelle_citation')
def nouvelle_citation():
    citation = random_citation(citations)
    return citation

# Fonction pour générer une citation aléatoire
def random_citation(citations):
    return random.choice(citations)

# Route pour afficher une erreur
@app.errorhandler(404)
def page_not_found(e):
    return 'Erreur 404 : page non trouvée', 404

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)

# Template HTML
@app.template_filter('strftime')
def _date_filter(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

# Fonction pour afficher les citations sous forme de tableau
@app.template_filter('citations_table')
def _citations_table(citations):
    return '<table><tr><th>Auteur</th><th>Citation</th></tr>' + ''.join(
        '<tr><td>{}</td><td>{}</td></tr>'.format(c['auteur'], c['citation']) for c in citations
    ) + '</table>'

# Route pour afficher les citations sous forme de tableau
@app.route('/citations')
def citations():
    return render_template('citations.html', citations=citations)
