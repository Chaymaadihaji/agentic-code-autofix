import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Chargement des données CSV
@st.cache
def charger_donnes():
    return pd.read_csv('donnees.csv')

# Fonction pour afficher les graphiques
def afficher_graphiques(df):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    sns.scatterplot(ax=axs[0, 0], x='A', y='B', data=df)
    sns.barplot(ax=axs[0, 1], x='C', y='D', data=df)
    sns.lineplot(ax=axs[1, 0], x='E', y='F', data=df)
    sns.boxplot(ax=axs[1, 1], x='G', y='H', data=df)
    st.pyplot(fig)

# Fonction pour appliquer les filtres
def appliquer_filtres(df):
    filtres = {'A': st.selectbox('Sélectionner une valeur pour A', df['A'].unique()),
               'B': st.selectbox('Sélectionner une valeur pour B', df['B'].unique())}
    return df[df['A'] == filtres['A'] & df['B'] == filtres['B']]

# Fonction pour calculer les statistiques
def calculer_statistiques(df):
    st.write('Statistiques :')
    st.write('Moyenne : ', df['A'].mean())
    st.write('Médiane : ', df['A'].median())
    st.write('Écart-type : ', df['A'].std())

# Fonction pour exporter les données
def exporter_donnes(df):
    st.download_button('Télécharger les données', data=df.to_csv(index=False), file_name='donnees.csv')

# Fonction pour afficher le dashboard
def afficher_dashboard():
    st.title('Dashboard')
    df = charger_donnes()
    st.write('Données chargées : ', df.shape)
    st.write('Données :')
    st.write(df.head())
    afficher_graphiques(df)
    filtres = appliquer_filtres(df)
    st.write('Données filtrées :')
    st.write(filtres.head())
    calculer_statistiques(df)
    exporter_donnes(df)

# Lancement de l'application
if __name__ == '__main__':
    st.title('Application Streamlit')
    afficher_dashboard()
