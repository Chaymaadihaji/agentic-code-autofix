# dashboard.py

import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

# URL de l'API météo
API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Ville de référence
VILLE = 'Paris'

# Paramètres de requête
PARAMS = {
    'q': VILLE,
    'appid': 'votre_api_key',
    'units': 'metric'
}

# Fonction pour récupérer les données météo en temps réel
def get_meteo_data():
    response = requests.get(API_URL, params=PARAMS)
    return response.json()

# Fonction pour calculer les statistiques/métriques
def calcul_statistiques(meteo_data):
    temp = meteo_data['main']['temp']
    hum = meteo_data['main']['humidity']
    return {
        'temp': temp,
        'hum': hum
    }

# Fonction pour générer les graphiques
def generer_graphiques(meteo_data):
    temps = [meteo_data['main']['temp']]
    hum = [meteo_data['main']['humidity']]
    plt.plot(temps, label='Température')
    plt.plot(hum, label='Humidité')
    plt.legend()
    plt.show()

# Fonction pour afficher les cartes météo
def afficher_cartes(meteo_data):
    carte = f"""
    <div class="card">
        <h5 class="card-title">Carte météo</h5>
        <div class="card-body">
            <p class="card-text">Température : {meteo_data['main']['temp']}°C</p>
            <p class="card-text">Humidité : {meteo_data['main']['humidity']}%</p>
        </div>
    </div>
    """
    return carte

# Route pour afficher les données météo en temps réel
@app.route('/')
def index():
    meteo_data = get_meteo_data()
    statistiques = calcul_statistiques(meteo_data)
    carte = afficher_cartes(meteo_data)
    return render_template('index.html', statistiques=statistiques, carte=carte)

# Route pour afficher les prévisions météo
@app.route('/previsions')
def previsions():
    return 'Prévisions météo'

# Route pour afficher les cartes météo
@app.route('/cartes')
def cartes():
    return 'Cartes météo'

# Fonction de démarrage
def start_app():
    app.run(debug=True)

if __name__ == "__main__":
    start_app()
