import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

# Choisir un fichier CSV à charger
@st.cache
def charger_donnes(file):
    return pd.read_csv(file)

# Choisir un fichier JSON à charger
@st.cache
def charger_parametres(file):
    with open(file, 'r') as f:
        return json.load(f)

# Calcul des statistiques
def calcul_statistiques(df):
    moyenne = df.mean().mean()
    mediane = df.median().median()
    std = df.std().std()
    return moyenne, mediane, std

# Créer un graphique en fonction des données sélectionnées
def creer_graphique(df, x, y):
    fig = go.Figure(data=[go.Scatter(x=df[x], y=df[y])])
    return fig

# Page de bienvenue
st.title('Analyse de données')

# Chargement des données CSV
st.header('Chargement des données')
file = st.file_uploader('Charger un fichier CSV', type='csv')
if file is not None:
    df = charger_donnes(file)

# Chargement des paramètres
st.header('Paramètres')
file = st.file_uploader('Charger un fichier JSON', type='json')
if file is not None:
    parametres = charger_parametres(file)

# Sélection des colonnes pour le graphique
st.header('Graphique')
x = st.selectbox('X', df.columns)
y = st.selectbox('Y', df.columns)

# Créer le graphique
if st.button('Créer le graphique'):
    fig = creer_graphique(df, x, y)
    st.plotly_chart(fig, use_container_width=True)

# Calcul des statistiques
st.header('Statistiques')
if df is not None:
    moyenne, mediane, std = calcul_statistiques(df)
    st.write(f'Moyenne : {moyenne}')
    st.write(f'Médiane : {mediane}')
    st.write(f'Écart-type : {std}')

# Page de filtres
st.title('Filtres')
if df is not None:
    # Filtre basé sur la valeur de la colonne sélectionnée
    col = st.selectbox('Colonne', df.columns)
    valeur = st.number_input('Valeur', min_value=df[col].min(), max_value=df[col].max())
    if st.button('Filtrer'):
        df_filtre = df[df[col] == valeur]
        st.write(df_filtre)

# Lancement de l'application
if __name__ == "__main__":
    st.run()
