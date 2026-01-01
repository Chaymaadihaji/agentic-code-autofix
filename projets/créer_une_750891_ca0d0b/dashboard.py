import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Chemin vers le dossier où sont stockés les fichiers CSV
CSV_DIR = 'donnees'

# Liste des noms de fichiers CSV
CSV_FILES = ['donnees_1.csv', 'donnees_2.csv']

# Fonction pour charger les données CSV
@st.cache
def charger_donnees():
    donnees = []
    for fichier in CSV_FILES:
        donnees.extend(pd.read_csv(f'{CSV_DIR}/{fichier}'))
    return pd.DataFrame(donnees)

# Fonction pour générer des graphiques interactifs
def generer_graphiques(donnees):
    fig, ax = plt.subplots()
    sns.scatterplot(x=donnees['A'], y=donnees['B'], ax=ax)
    ax.set_title('Graphique interactif')
    return fig

# Fonction pour calculer les statistiques
def calculer_statistiques(donnees):
    return donnees.describe()

# Fonction pour afficher les résultats
def afficher_résultats(donnees, statistiques, graphiques):
    st.write('Données chargées avec succès')
    st.write('Statistiques:')
    st.write(statistiques)
    st.write('Graphiques:')
    st.pyplot(graphiques)

# Fonction de lancement de l'application
def lancer_application():
    donnees = charger_donnees()
    st.title('Dashboard')
    st.write('Filtres:')
    filtres = st.selectbox('Sélectionner un filtre', ['Tous', 'Filtre 1', 'Filtre 2'])
    if filtres == 'Tous':
        donnees_filtrees = donnees
    else:
        donnees_filtrees = donnees[donnees['C'] == filtres]
    st.write('Données filtrées:')
    st.write(donnees_filtrees)
    st.write('Statistiques:')
    st.write(calculer_statistiques(donnees_filtrees))
    st.write('Graphiques:')
    graphiques = generer_graphiques(donnees_filtrees)
    afficher_résultats(donnees_filtrees, calculer_statistiques(donnees_filtrees), graphiques)

# Lancement de l'application
if __name__ == "__main__":
    lancer_application()
