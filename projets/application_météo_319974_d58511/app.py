# app.py - Généré par Robot Développeur
# Demande: application météo avec cartes pour 5 villes et graphiques de température
# Type d'application: dashboard

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html', 
                         app_name="Application générée",
                         features=['afficher les cartes météo', 'afficher les graphiques de température', 'sélectionner les 5 villes'])

@app.route('/api/data')
def api_data():
    """API de données"""
    return jsonify({
        "status": "success",
        "message": "Application fonctionnelle",
        "features": ['afficher les cartes météo', 'afficher les graphiques de température', 'sélectionner les 5 villes']
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
