# config.py

# Importation des bibliothèques nécessaires
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json

# Définition des constantes
VILLES = ["Paris", "Lyon", "Marseille", "Bordeaux", "Toulouse"]
API_KEY = "YOUR_API_KEY_HERE"

# Chargement des données météo
def charger_donnees(ville):
    # Simuler les données météo pour chaque ville
    donnees = {
        "Paris": {"temperature": 20, "humidite": 60},
        "Lyon": {"temperature": 22, "humidite": 50},
        "Marseille": {"temperature": 25, "humidite": 40},
        "Bordeaux": {"temperature": 18, "humidite": 70},
        "Toulouse": {"temperature": 20, "humidite": 60},
    }
    return donnees[ville]

# Création de l'application Dash
app = dash.Dash(__name__)

# Définition de la structure de l'application
app.layout = html.Div(
    children=[
        html.H1(children="Application Météo"),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H2(children=ville),
                        html.P(children=f"Température: {charger_donnees(ville)['temperature']}°C"),
                        html.P(children=f"Humidité: {charger_donnees(ville)['humidite']}%"),
                    ],
                    className="carte",
                )
                for ville in VILLES
            ],
            className="grid",
        ),
        dcc.Graph(id="graph-temperature"),
        dcc.Dropdown(
            id="ville-dropdown",
            options=[{"label": ville, "value": ville} for ville in VILLES],
            value=VILLES[0],
        ),
    ]
)

# Mise à jour du graphique de température
@app.callback(
    Output("graph-temperature", "figure"),
    [Input("ville-dropdown", "value")],
)
def mettre_a_jour_graph(ville):
    donnees = charger_donnees(ville)
    fig = px.bar(x=["Température", "Humidité"], y=[donnees["temperature"], donnees["humidite"]])
    return fig

# Lancement de l'application
if __name__ == "__main__":
    app.run_server(debug=True)
