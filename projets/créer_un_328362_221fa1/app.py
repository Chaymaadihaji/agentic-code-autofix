from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

app = Flask(__name__)
Bootstrap(app)

# Génération de données pour le dashboard
donnees = {
    "Tâches": ["Tâche 1", "Tâche 2", "Tâche 3"],
    "Statut": ["En cours", "Terminé", "En cours"],
    "Période": ["2022-01-01", "2022-01-15", "2022-02-01"]
}

df = pd.DataFrame(donnees)

# Calcul des statistiques/métriques
stats = df["Statut"].value_counts().to_dict()

# API pour les données en temps réel
@app.route("/donnees", methods=["GET"])
def donnees_api():
    return jsonify(df.to_dict(orient="records"))

# Route pour le dashboard
@app.route("/")
def index():
    return render_template("index.html")

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
