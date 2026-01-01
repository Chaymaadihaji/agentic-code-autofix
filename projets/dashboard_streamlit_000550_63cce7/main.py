python
# main.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données
@st.cache
def charger_donnes():
    try:
        donnees = pd.read_csv('donnees.csv')
        return donnees
    except Exception as e:
        print(f"Erreur de chargement des données : {e}")
        return None

# Fonction de visualisation
def visualiser donnees:
    try:
        # Création d'un graphique avec Plotly Express
        fig = px.bar(donnees, x='Variable', y='Valeur')
        return fig
    except Exception as e:
        print(f"Erreur de visualisation : {e}")
        return None

# Fonction principale
def main():
    # Chargement des données
    donnees = charger_donnes()
    
    # Si les données ont été chargées avec succès
    if donnees is not None:
        # Affichage du menu
        menu = ["Visualisation", "Informations"]
        selection = st.sidebar.selectbox("Choisissez une option", menu)
        
        # Traitement en fonction de la sélection
        if selection == "Visualisation":
            # Affichage du graphique
            st.title("Visualisation")
            fig = visualiser(donnees)
            if fig is not None:
                st.plotly_chart(fig)
        elif selection == "Informations":
            # Affichage des informations
            st.title("Informations")
            st.write("Données chargées avec succès")
            st.write(donnees.head())
    else:
        # Affichage d'une erreur si les données n'ont pas été chargées
        st.error("Erreur de chargement des données")

# Exécution de la fonction principale
if __name__ == "__main__":
    main()
