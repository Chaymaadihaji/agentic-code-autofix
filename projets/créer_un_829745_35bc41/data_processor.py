# data_processor.py

import pandas as pd
import requests
import json
from flask import Flask, render_template
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool

app = Flask(__name__)

# Génération de données pour le dashboard
def generer_donnees_meteo():
    donnees = {
        'temperature': [23, 25, 22, 24, 26],
        'humidite': [60, 55, 65, 58, 62],
        'pression': [1013, 1015, 1012, 1014, 1016]
    }
    return pd.DataFrame(donnees)

# Calcul des statistiques/métriques
def calcul_statistiques(df):
    statistiques = {
        'moyenne_temperature': df['temperature'].mean(),
        'moyenne_humidite': df['humidite'].mean(),
        'moyenne_pression': df['pression'].mean()
    }
    return pd.Series(statistiques)

# API pour les données en temps réel
def obtenir_donnees_temporelles():
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Paris&appid=YOUR_API_KEY'
    response = requests.get(url)
    return response.json()

# Générer les graphiques
def generer_graphiques(df):
    p = figure(title="Graphique de la température",
               x_axis_label='Date',
               y_axis_label='Température')
    p.line(df.index, df['temperature'], legend_label="Température", line_width=2)
    p.line(df.index, df['humidite'], legend_label="Humidité", line_width=2)
    p.line(df.index, df['pression'], legend_label="Pression", line_width=2)
    script, div = components(p)
    return script, div

# Générer les cartes
def generer_cartes(df):
    p = figure(title="Carte de la météo",
               x_axis_label='Longitude',
               y_axis_label='Latitude')
    p.circle([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], size=10)
    script, div = components(p)
    return script, div

# Route pour le dashboard
@app.route('/')
def index():
    df = generer_donnees_meteo()
    statistiques = calcul_statistiques(df)
    donnees_temporelles = obtenir_donnees_temporelles()
    script, div = generer_graphiques(df)
    script_cartes, div_cartes = generer_cartes(df)
    return render_template('index.html', script=script, div=div, script_cartes=script_cartes, div_cartes=div_cartes, statistiques=statistiques, donnees_temporelles=donnees_temporelles)

if __name__ == "__main__":
    app.run(debug=True)
