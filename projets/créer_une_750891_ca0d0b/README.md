import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Chargement des données CSV
@st.cache
def load_data(file):
    return pd.read_csv(file)

# Affichage des graphiques interactifs
def display_graphs(df):
    st.title("Graphiques")
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(10,6))
        plt.plot(df["col1"])
        st.pyplot(plt.gcf())
    with col2:
        plt.figure(figsize=(10,6))
        plt.scatter(df["col1"], df["col2"])
        st.pyplot(plt.gcf())

# Application des filtres
def apply_filters(df):
    st.title("Filtres")
    col1, col2 = st.columns(2)
    with col1:
        min_value = st.number_input("Minimum", value=0)
        max_value = st.number_input("Maximum", value=100)
    with col2:
        filter_col = st.selectbox("Filtrer par", df.columns)
        filter_value = st.number_input("Valeur", value=0)
    filtered_df = df[(df[filter_col] >= min_value) & (df[filter_col] <= max_value) & (df[filter_col] == filter_value)]
    return filtered_df

# Calcul des statistiques
def calculate_stats(df):
    st.title("Statistiques")
    st.write("Mean:", df.mean().mean())
    st.write("Median:", df.median().median())
    st.write("Standard Deviation:", df.std().std())

# Gestion des erreurs
def handle_error(e):
    st.title("Erreur")
    st.write(e)

# Fonction principale
def main():
    st.title("Créer une application Streamlit pour visualiser et analyser des données CSV")
    file = st.file_uploader("Charger des données CSV")
    if file:
        data = load_data(file)
        display_graphs(data)
        filtered_data = apply_filters(data)
        calculate_stats(data)
    else:
        handle_error("Aucune donnée chargée")

if __name__ == "__main__":
    main()
