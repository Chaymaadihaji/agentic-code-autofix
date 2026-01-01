import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Chargement des données CSV
@st.cache
def charger_donnees():
    return pd.read_csv('donnees.csv')

# Fonction pour afficher les graphiques interactifs
def afficher_graphiques(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    sns.scatterplot(data=df, x='Variable1', y='Variable2', ax=axes[0])
    sns.barplot(data=df, x='Variable1', y='Variable2', ax=axes[1])
    st.pyplot(fig)

# Fonction pour appliquer les filtres
def appliquer_filtres(df):
    st.write('Filtres')
    col1, col2 = st.columns(2)
    with col1:
        var1 = st.selectbox('Variable 1', df.columns)
    with col2:
        var2 = st.selectbox('Variable 2', df.columns)
    return df[(df[var1] > 0) & (df[var2] > 0)]

# Fonction pour calculer les statistiques
def calcul_statistiques(df):
    st.write('Statistiques')
    st.write('Moyenne:', df.mean().mean())
    st.write('Écart-type:', df.std().std())

# Main
if __name__ == "__main__":
    st.title('Dashboard')
    df = charger_donnees()
    st.write('Données')
    st.write(df.head())

    # Afficher les graphiques interactifs
    afficher_graphiques(df)

    # Appliquer les filtres
    df_filtres = appliquer_filtres(df)
    st.write('Données filtrées')
    st.write(df_filtres.head())

    # Calculer les statistiques
    calcul_statistiques(df_filtres)
