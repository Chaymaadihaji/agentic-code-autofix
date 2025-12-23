# models.py

import os
from flask import Flask, render_template, jsonify
from random import choice
import json

app = Flask(__name__)

# Chemin du fichier JSON contenant les citations
CITATIONS_FILE = 'citations.json'

# Chargement des citations depuis le fichier JSON
with open(CITATIONS_FILE, 'r') as f:
    citations = json.load(f)

# Fonction pour générer une citation aléatoire
def generate_citation():
    return choice(citations)

# Route pour afficher la citation aléatoire
@app.route('/')
def index():
    citation = generate_citation()
    return render_template('index.html', citation=citation)

# Route pour générer une nouvelle citation (API)
@app.route('/citation', methods=['GET'])
def new_citation():
    citation = generate_citation()
    return jsonify({'citation': citation})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
