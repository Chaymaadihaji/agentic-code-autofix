#!/usr/bin/env python3
"""
🚑 Réparateur de projet météo
"""

import os
import shutil

def reparer_projet_meteo(chemin_projet):
    """Réparer complètement le projet météo"""
    print(f"🔧 Réparation de: {chemin_projet}")
    
    # 1. Remplacer main.py par un fichier fonctionnel
    main_py = '''# main.py - Application météo FONCTIONNELLE
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Données fixes pour 5 villes (évite les APIs externes)
VILLES = [
    {"nom": "Paris", "temp": 15, "hum": 65, "desc": "Nuageux"},
    {"nom": "Lyon", "temp": 18, "hum": 60, "desc": "Ensoleillé"},
    {"nom": "Marseille", "temp": 22, "hum": 55, "desc": "Clair"},
    {"nom": "Bordeaux", "temp": 17, "hum": 70, "desc": "Pluvieux"},
    {"nom": "Lille", "temp": 12, "hum": 75, "desc": "Brumeux"}
]

@app.route('/')
def index():
    return render_template('index.html', villes=VILLES)

@app.route('/api/data')
def api_data():
    return jsonify(VILLES)

if __name__ == '__main__':
    print("✅ Application Météo FONCTIONNELLE")
    print("🌐 Accès: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
'''
    
    with open(os.path.join(chemin_projet, "main.py"), "w", encoding="utf-8") as f:
        f.write(main_py)
    
    # 2. Créer un template HTML SIMPLE et VALIDE
    template_dir = os.path.join(chemin_projet, "templates")
    os.makedirs(template_dir, exist_ok=True)
    
    index_html = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Météo - 5 Villes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; background: #f0f8ff; }
        .ville-card { 
            background: white; 
            padding: 15px; 
            margin: 10px; 
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .temp { font-size: 2em; color: #e74c3c; font-weight: bold; }
        .ville-nom { color: #2c3e50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">🌤️ Météo 5 Villes</h1>
        <div class="row">
            {% for ville in villes %}
            <div class="col-md-2">
                <div class="ville-card text-center">
                    <div class="ville-nom">{{ ville.nom }}</div>
                    <div class="temp">{{ ville.temp }}°C</div>
                    <div>{{ ville.desc }}</div>
                    <small>💧 {{ ville.hum }}%</small>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="mt-5">
            <h3>📊 Graphique de température</h3>
            <canvas id="tempChart" width="400" height="200"></canvas>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const villes = {{ villes|tojson }};
        const ctx = document.getElementById('tempChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: villes.map(v => v.nom),
                datasets: [{
                    label: 'Température °C',
                    data: villes.map(v => v.temp),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)'
                }]
            }
        });
    </script>
</body>
</html>'''
    
    with open(os.path.join(template_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    
    # 3. Créer requirements.txt minimal
    with open(os.path.join(chemin_projet, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write("Flask==2.3.3\nrequests==2.31.0\n")
    
    print(f"✅ Projet réparé: {chemin_projet}")
    print(f"📁 Fichiers créés:")
    print(f"   - main.py (application Flask fonctionnelle)")
    print(f"   - templates/index.html (template valide)")
    print(f"   - requirements.txt (dépendances minimales)")
    print(f"\n🚀 POUR TESTER: cd '{chemin_projet}' && python main.py")

if __name__ == "__main__":
    # Réparer le dernier projet créé
    import glob
    projets = glob.glob("projets/*")
    if projets:
        dernier_projet = max(projets, key=os.path.getctime)
        reparer_projet_meteo(dernier_projet)
    else:
        print("❌ Aucun projet trouvé dans 'projets/'")