from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html', 
                         app_name="Application générée",
                         message="Application fonctionnelle générée automatiquement")

@app.route('/api/status')
def api_status():
    """API de statut"""
    return jsonify({
        "status": "success",
        "message": "Application Flask fonctionnelle",
        "features": ["Interface web", "API REST", "Design responsive"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
