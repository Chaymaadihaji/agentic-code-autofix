import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Données
donnees = {
    'Nom': ['John', 'Anna', 'Peter', 'Linda'],
    'Age': [28, 24, 35, 32],
    'Ville': ['Paris', 'Lyon', 'Marseille', 'Bordeaux']
}

# Création du DataFrame
df = pd.DataFrame(donnees)

# Fonction pour afficher les données
def afficher_donnees(df):
    st.header('Données')
    st.write(df)

# Fonction pour afficher les graphiques
def afficher_graphiques(df):
    st.header('Graphiques')
    fig, ax = plt.subplots()
    ax.plot(df['Age'])
    ax.set_xlabel('Nom')
    ax.set_ylabel('Age')
    st.pyplot(fig)

# Interface utilisateur
st.title('Calculatrice')

# Filtre
filtre_ville = st.selectbox('Ville', df['Ville'].unique())

# Formulaire
nom = st.text_input('Nom')
age = st.number_input('Age', min_value=0)

# Bouton pour afficher les données filtrées
if st.button('Afficher données'):
    df_filtre = df[df['Ville'] == filtre_ville]
    st.write(df_filtre)

# Bouton pour afficher les graphiques
if st.button('Afficher graphiques'):
    afficher_graphiques(df)

# Dashboard
st.header('Dashboard')
st.write('Bonjour !')

# Filtre pour les graphiques
filtre_age = st.selectbox('Age', df['Age'].unique())

# Graphique
if st.button('Afficher graphique'):
    fig, ax = plt.subplots()
    ax.plot(df['Nom'], df['Age'])
    ax.set_xlabel('Nom')
    ax.set_ylabel('Age')
    st.pyplot(fig)

# Filtre pour les données
filtre_nom = st.selectbox('Nom', df['Nom'].unique())

# Données filtrées
if st.button('Afficher données'):
    df_filtre = df[df['Nom'] == filtre_nom]
    st.write(df_filtre)

# Lancement de l'application
if __name__ == "__main__":
    st.run()
