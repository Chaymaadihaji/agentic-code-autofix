# data_processor.py

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Chargement des données CSV
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

# Calcul des statistiques
def calculate_statistics(df):
    mean = df.mean().mean()
    median = df.median().mean()
    std = df.std().mean()
    return mean, median, std

# API pour les données en temps réel
def get_realtime_data():
    with open('data.json') as file:
        return json.load(file)

# Structure modulaire pour différentes visualisations
def draw_bar_chart(df, title):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df)
    plt.title(title)
    return plt

# Structure modulaire pour différentes visualisations
def draw_line_chart(df, title):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df)
    plt.title(title)
    return plt

# Application
def app():
    st.title('Dashboard')
    
    # Menu principal
    selected_option = option_menu(
        menu_title="Outils",
        options=["Filtres", "Statistiques", "Graphiques", "Tableaux", "Export"],
        icons=["filter", "graph", "table", "download"],
        horizontal=True
    )
    
    # Filtres
    if selected_option == "Filtres":
        st.header("Filtres")
        df = load_data('data.csv')
        st.write(df)
        
        # Application de filtres
        col1, col2 = st.columns(2)
        with col1:
            filtre1 = st.selectbox("Filtre 1", df['column1'].unique())
        with col2:
            filtre2 = st.selectbox("Filtre 2", df['column2'].unique())
        
        # Affichage des données filtrées
        df_filtre = df[(df['column1'] == filtre1) & (df['column2'] == filtre2)]
        st.write(df_filtre)
    
    # Statistiques
    elif selected_option == "Statistiques":
        st.header("Statistiques")
        df = load_data('data.csv')
        mean, median, std = calculate_statistics(df)
        st.write(f"Moyenne : {mean}")
        st.write(f"Médiane : {median}")
        st.write(f"Écart-type : {std}")
    
    # Graphiques
    elif selected_option == "Graphiques":
        st.header("Graphiques")
        df = load_data('data.csv')
        
        # Bar chart
        col1, col2 = st.columns(2)
        with col1:
            st.write(draw_bar_chart(df, 'Bar Chart'))
        with col2:
            st.write(draw_line_chart(df, 'Line Chart'))
    
    # Tableaux
    elif selected_option == "Tableaux":
        st.header("Tableaux")
        df = load_data('data.csv')
        st.write(df)
    
    # Export
    elif selected_option == "Export":
        st.header("Export")
        df = load_data('data.csv')
        st.download_button(
            label="Télécharger les données",
            data=df.to_csv(index=False),
            file_name='data.csv',
            mime='text/csv'
        )
    
    # Données en temps réel
    elif selected_option == "Données en temps réel":
        st.header("Données en temps réel")
        df = get_realtime_data()
        st.write(df)

if __name__ == "__main__":
    app()
