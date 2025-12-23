import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Données de test
taches = [
    {"nom": "Tâche 1", "statut": "en attente"},
    {"nom": "Tâche 2", "statut": "en cours"},
    {"nom": "Tâche 3", "statut": "terminée"}
]

# Tableau de données
df = pd.DataFrame(taches)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Gestionnaire de Tâches"),
    html.Div([
        html.H2("Liste des tâches"),
        html.Table([
            html.Tr([html.Th("Nom"), html.Th("Statut")]),
            html.Tbody([
                html.Tr([html.Td(tache["nom"]), html.Td(tache["statut"])]) for tache in taches
            ])
        ])
    ]),
    html.Div([
        html.H2("Statistiques"),
        html.Div([
            html.H3("Nombre de tâches en attente:"),
            html.P(str(df[df["statut"] == "en attente"].shape[0])),
            html.H3("Nombre de tâches en cours:"),
            html.P(str(df[df["statut"] == "en cours"].shape[0])),
            html.H3("Nombre de tâches terminées:"),
            html.P(str(df[df["statut"] == "terminée"].shape[0]))
        ])
    ]),
    dcc.Graph(
        id="statut-tache",
        figure=px.bar(df, x="nom", y="statut", color="statut", barmode="group")
    ),
    html.Div([
        html.H2("Créer une nouvelle tâche"),
        html.Form([
            html.Label("Nom de la tâche"),
            dcc.Input(id="nom-tache", type="text"),
            html.Br(),
            html.Label("Statut de la tâche"),
            dcc.Dropdown(id="statut-tache", options=[
                {"label": "en attente", "value": "en attente"},
                {"label": "en cours", "value": "en cours"},
                {"label": "terminée", "value": "terminée"}
            ]),
            html.Br(),
            html.Button("Ajouter", id="ajouter-tache"),
            html.Div(id="resultat")
        ])
    ])
])

@app.callback(
    Output("resultat", "children"),
    [Input("ajouter-tache", "n_clicks")]
)
def ajouter_tache(n_clicks):
    if n_clicks:
        nom_tache = app.callback_context.inputs.nom_tache.value
        statut_tache = app.callback_context.inputs.statut_tache.value
        taches.append({"nom": nom_tache, "statut": statut_tache})
        df = pd.DataFrame(taches)
        return html.P(f"Tâche ajoutée: {nom_tache} ({statut_tache})")

if __name__ == "__main__":
    app.run_server(debug=True)
