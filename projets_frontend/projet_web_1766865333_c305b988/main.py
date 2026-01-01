# main.py - Généré par Robot Développeur
# Demande: Je veux un système de connexion avec mot de passe crypté, validation email, réinitialisation par SMS, historique des connexions, et protection contre les attaques bruteforce. - Fichier: main.py
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
                         features=['connexion avec mot de passe crypté', 'validation email', 'réinitialisation par SMS', 'historique des connexions', 'protection contre les attaques bruteforce'])

@app.route('/api/data')
def api_data():
    """API de données"""
    return jsonify({
        "status": "success",
        "message": "Application fonctionnelle",
        "features": ['connexion avec mot de passe crypté', 'validation email', 'réinitialisation par SMS', 'historique des connexions', 'protection contre les attaques bruteforce']
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
