# main.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json

# Chargement des données météo
with open('donnees_meteo.json') as f:
    donnees_meteo = json.load(f)

# Création d'un dataframe pour les données météo
df = pd.DataFrame(donnees_meteo)

# Sélection des 5 villes
villes = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse']

# Création de l'application Dash
app = dash.Dash(__name__)

# Définition de la mise en page
app.layout = html.Div([
    html.H1('Application Météo'),
    html.P('Sélectionnez une ville pour afficher les données météo'),
    dcc.Dropdown(
        id='ville-dropdown',
        options=[{'label': ville, 'value': ville} for ville in villes],
        value=villes[0]
    ),
    html.Div([
        html.Div([
            html.H2('Carte Météo'),
            html.Img(id='carte-meteo', src='carte_meteo.png')
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.H2('Graphique de Température'),
            dcc.Graph(id='graph-temperature')
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
])

# Callback pour mettre à jour le graphique de température
@app.callback(
    Output('graph-temperature', 'figure'),
    [Input('ville-dropdown', 'value')]
)
def update_graph(ville):
    # Filtrer les données pour la ville sélectionnée
    df_ville = df[df['ville'] == ville]
    
    # Créer le graphique de température
    fig = px.line(df_ville, x='date', y='temperature')
    return fig

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)