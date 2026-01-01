# app.py
import json
import random
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

app = Flask(__name__)
Bootstrap(app)

# Fichier JSON contenant les données météo
with open('donnees_meteo.json') as f:
    donnees_meteo = json.load(f)

# Calcul des statistiques/métriques
def calcul_statistiques(donnees):
    temperature_moyenne = sum(donnees['temperature']) / len(donnees['temperature'])
    pluie_moyenne = sum(donnees['pluie']) / len(donnees['pluie'])
    return temperature_moyenne, pluie_moyenne

# Génération de données pour le dashboard
donnees_dashboard = {
    'temperature': [random.randint(15, 30) for _ in range(24)],
    'pluie': [random.random() for _ in range(24)],
}

# Calcul des statistiques/métriques
temperature_moyenne, pluie_moyenne = calcul_statistiques(donnees_dashboard)

# API pour les données en temps réel
@app.route('/donnees')
def donnees_api():
    return jsonify({'temperature': donnees_dashboard['temperature'], 'pluie': donnees_dashboard['pluie']})

# Route pour la page de dashboard
@app.route('/')
def index():
    return render_template('index.html', temperature_moyenne=temperature_moyenne, pluie_moyenne=pluie_moyenne)

# Route pour les graphiques
@app.route('/graphiques')
def graphiques():
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=pd.DataFrame({'temps': range(24), 'temperature': donnees_dashboard['temperature']}))
    plt.xlabel('Temps')
    plt.ylabel('Température')
    plt.title('Évolution de la température')
    plt.savefig('static/graphiques.png')
    return 'Graphiques générés'

# Route pour les cartes
@app.route('/cartes')
def cartes():
    return render_template('cartes.html')

if __name__ == "__main__":
    app.run(debug=True)

# index.html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard météo</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Dashboard météo</a>
    </nav>
    <div class="container">
        <h1>État météo actuel</h1>
        <p>Température moyenne : {{ temperature_moyenne }}°C</p>
        <p>Pluie moyenne : {{ pluie_moyenne }}%</p>
    </div>
    <img src="{{ url_for('static', filename='graphiques.png') }}" alt="Graphiques">
</body>
</html>

# cartes.html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cartes météo</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Cartes météo</a>
    </nav>
    <div class="container">
        <h1>Cartes météo</h1>
        <p>Cliquez sur les cartes pour afficher les informations détaillées</p>
    </div>
</body>
</html>
