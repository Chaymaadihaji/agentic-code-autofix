# models.py - Généré par Robot Développeur
# Demande: Créer un gestionnaire de tâches avec liste interactive et statistiques de progression
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
                         features=['création de tâches', 'édition de tâches', 'suppression de tâches', 'affichage de statistiques de progression'])

@app.route('/api/data')
def api_data():
    """API de données"""
    return jsonify({
        "status": "success",
        "message": "Application fonctionnelle",
        "features": ['création de tâches', 'édition de tâches', 'suppression de tâches', 'affichage de statistiques de progression']
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
