import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Chargement des données CSV
@st.cache
def load_data(file):
    return pd.read_csv(file)

# Fonction pour afficher les graphiques interactifs
def show_graphs(df):
    st.subheader("Graphiques")
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    sns.set()
    sns.scatterplot(x="A", y="B", data=df, ax=axs[0, 0])
    sns.barplot(x="C", y="D", data=df, ax=axs[0, 1])
    sns.lineplot(x="E", y="F", data=df, ax=axs[1, 0])
    sns.kdeplot(x="G", data=df, ax=axs[1, 1])
    st.pyplot(fig)

# Fonction pour appliquer les filtres
def apply_filters(df):
    st.subheader("Filtres")
    col1, col2 = st.columns(2)
    filtres = col1.selectbox("Choisir un filtre", ["Tous", "Filtre 1", "Filtre 2"])
    if filtres == "Filtre 1":
        df = df[df["H"] == "Valeur 1"]
    elif filtres == "Filtre 2":
        df = df[df["I"] == "Valeur 2"]
    return df

# Fonction pour calculer les statistiques
def calculate_stats(df):
    st.subheader("Statistiques")
    stats = df.describe()
    st.write(stats)

# Fonction pour exporter les données
def export_data(df):
    st.subheader("Exporter les données")
    file_download = st.button("Télécharger les données")
    if file_download:
        df.to_csv("donnees.csv", index=False)
        st.success("Les données ont été téléchargées")

# Fonction pour générer le dashboard
def generate_dashboard():
    st.title("Dashboard")
    st.subheader("Données")
    file = st.file_uploader("Uploader un fichier CSV", type=["csv"])
    if file:
        df = load_data(file)
        st.write(df)
        st.write("Nombre de lignes : ", len(df))
        st.write("Nombre de colonnes : ", len(df.columns))
        show_graphs(df)
        filtered_df = apply_filters(df)
        st.write(filtered_df)
        calculate_stats(filtered_df)
        export_data(filtered_df)

if __name__ == "__main__":
    generate_dashboard()
