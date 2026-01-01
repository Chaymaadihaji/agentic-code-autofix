import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from flask import Flask
from flask import render_template
from dash_extensions import Graph

app = Flask(__name__)

# Génération de données
np.random.seed(0)
donnees_meteo = {
    'date': pd.date_range('2022-01-01', '2022-01-31'),
    'temperature': np.random.uniform(10, 20, 31),
    'humidite': np.random.uniform(60, 80, 31),
    'vent': np.random.uniform(5, 15, 31)
}

# Calcul des statistiques/métriques
statistiques = {
    'temperature_moyenne': donnees_meteo['temperature'].mean(),
    'humidite_moyenne': donnees_meteo['humidite'].mean(),
    'vent_moyen': donnees_meteo['vent'].mean()
}

# API pour les données en temps réel
def get_donnees_meteo():
    return {
        'temperature': np.random.uniform(10, 20),
        'humidite': np.random.uniform(60, 80),
        'vent': np.random.uniform(5, 15)
    }

# Structure modulaire pour différentes visualisations
def creer_graphique(data):
    fig = px.line(data, x='date', y='temperature')
    return fig

# Interface web
@app.route('/')
def index():
    return render_template('index.html')

# Lancement de l'app
if __name__ == "__main__":
    app.run_server(debug=True)
