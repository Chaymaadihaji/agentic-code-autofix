import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime

# Chargement de données CSV
@st.cache
def load_data(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error("Erreur lors du chargement des données : " + str(e))

# Génération de données pour le dashboard
def generate_data():
    data = {
        "date": [datetime(2022, 1, 1), datetime(2022, 1, 2), datetime(2022, 1, 3)],
        "valeur": [10, 20, 30]
    }
    return pd.DataFrame(data)

# Calcul des statistiques/métriques
def calculate_stats(data):
    stats = {
        "mean": data["valeur"].mean(),
        "median": data["valeur"].median(),
        "max": data["valeur"].max(),
        "min": data["valeur"].min()
    }
    return stats

# API pour les données en temps réel
def get_realtime_data():
    with open("data.json", "r") as f:
        return json.load(f)

# Structure modulaire pour différentes visualisations
def plot_line_chart(data):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="date", y="valeur", data=data)
    plt.title("Ligne de temps")
    plt.xlabel("Date")
    plt.ylabel("Valeur")
    return plt

# Structure modulaire pour différentes visualisations
def plot_bar_chart(data):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="date", y="valeur", data=data)
    plt.title("Barème")
    plt.xlabel("Date")
    plt.ylabel("Valeur")
    return plt

# Application
if __name__ == "__main__":
    st.title("Dashboard")

    # Chargement de données CSV
    file = st.file_uploader("Uploader un fichier CSV")
    if file:
        data = load_data(file.name)
        st.write(data)

    # Génération de données pour le dashboard
    data = generate_data()
    st.write(data)

    # Calcul des statistiques/métriques
    stats = calculate_stats(data)
    st.write("Statistiques :")
    st.write(stats)

    # API pour les données en temps réel
    realtime_data = get_realtime_data()
    st.write("Données en temps réel :")
    st.write(realtime_data)

    # Structure modulaire pour différentes visualisations
    select_box = st.selectbox("Sélectionner une visualisation", ["Ligne de temps", "Barème"])
    if select_box == "Ligne de temps":
        fig = plot_line_chart(data)
    elif select_box == "Barème":
        fig = plot_bar_chart(data)
    st.pyplot(fig)

    # Export de données
    if st.button("Exporter données"):
        st.download_button("Télécharger les données", data.to_csv(index=False), "data.csv", "text/csv")
