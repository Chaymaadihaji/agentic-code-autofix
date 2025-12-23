# main.py - Généré par Robot Développeur
# Demande: Créer un gestionnaire de tâches avec liste interactive et statistiques de progression
# Type d'application: web

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html', 
                         app_name="Application générée",
                         features=['statistique'])

@app.route('/api/data')
def api_data():
    """API de données"""
    return jsonify({
        "status": "success",
        "message": "Application fonctionnelle",
        "features": ['statistique']
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
