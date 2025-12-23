import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Génération de données
data = {
    'Nom': ['Tâche 1', 'Tâche 2', 'Tâche 3', 'Tâche 4', 'Tâche 5'],
    'Progression': [20, 50, 80, 30, 90]
}

df = pd.DataFrame(data)

# Création de l'application Dash
app = dash.Dash(__name__)

# Layout de l'application
app.layout = html.Div([
    html.H1('Gestionnaire de tâches'),
    html.Div([
        html.H2('Liste interactive des tâches'),
        dcc.Loading(id="loading-icon", type="default", children=[html.Div(id="loading-output")]),
        html.Div(id='tableau')
    ]),
    html.Div([
        html.H2('Statistiques de progression'),
        dcc.Graph(id='statistiques')
    ]),
    html.Div([
        html.H2('Filtrage et tri des tâches'),
        dcc.Dropdown(id='filtrage', options=[{'label': i, 'value': i} for i in df['Nom'].unique()]),
        html.Div(id='resultats')
    ])
])

# Création de la liste interactive des tâches
@app.callback(
    Output('tableau', 'children'),
    [Input('filtrage', 'value')]
)
def update_tableau(value):
    filtered_df = df[df['Nom'] == value]
    return html.Table([
        html.Thead(html.Tr([html.Th(col) for col in filtered_df.columns])),
        html.Tbody([html.Tr([html.Td(cell) for cell in row]) for row in filtered_df.to_numpy()])
    ])

# Calcul des statistiques de progression
@app.callback(
    Output('statistiques', 'figure'),
    [Input('filtrage', 'value')]
)
def update_statistiques(value):
    filtered_df = df[df['Nom'] == value]
    fig = px.bar(filtered_df, x='Nom', y='Progression')
    return fig

# Filtrage et tri des tâches
@app.callback(
    Output('resultats', 'children'),
    [Input('filtrage', 'value')]
)
def update_resultats(value):
    filtered_df = df[df['Nom'] == value]
    return html.Div([html.P(f"Progression : {filtered_df['Progression'].values[0]}%")])

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
