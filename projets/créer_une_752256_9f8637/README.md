import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Données pour l'exemple
data = {
    'Nom': ['John', 'Anna', 'Peter', 'Linda'],
    'Âge': [25, 32, 43, 28],
    'Ville': ['New York', 'Paris', 'Londres', 'Berlin']
}

# Chargement des données dans un DataFrame
df = pd.DataFrame(data)

# Page d'accueil
st.title('Application Streamlit')

# Formulaire pour saisir les critères de filtrage
st.write('Filtrage des données')
nom = st.text_input('Nom')
âge = st.slider('Âge', 0, 100)
ville = st.selectbox('Ville', ['New York', 'Paris', 'Londres', 'Berlin'])

# Bouton pour lancer le filtrage
if st.button('Filtrer'):
    filtered_df = df[(df['Nom'] == nom) & (df['Âge'] == âge) & (df['Ville'] == ville)]
    st.write(filtered_df)

# Graphique en temps réel
st.write('Graphique en temps réel')
st.line_chart(df['Âge'])

# Tableau des données
st.write('Tableau des données')
st.table(df)

# Galerie d'images
st.write('Galerie d\'images')
image1 = st.image('image1.jpg')
image2 = st.image('image2.jpg')

# Carte
st.write('Carte')
map_data = {
    'Latitude': [40.7128, 48.8566, 51.5074, 52.5200],
    'Longitude': [-74.0060, 2.3522, -0.1278, 13.4050]
}
map_df = pd.DataFrame(map_data)
st.map(map_df)
