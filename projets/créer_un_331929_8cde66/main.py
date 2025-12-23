# main.py

from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

# Fichier JSON contenant les citations
with open('citations.json', 'r') as f:
    citations = json.load(f)

@app.route('/')
def index():
    """Affiche une nouvelle citation à chaque rafraîchissement"""
    citation = random.choice(citations)
    return render_template('index.html', citation=citation)

@app.route('/nouveauecitation', methods=['POST'])
def nouvelle_citation():
    """Renvoie une nouvelle citation"""
    citation = random.choice(citations)
    return {'citation': citation}

if __name__ == "__main__":
    app.run(debug=True)
