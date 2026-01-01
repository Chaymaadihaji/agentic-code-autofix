python
# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
@st.cache
def load_data():
    data = pd.read_csv("data.csv")
    return data

# Fonction pour générer des visualisations
def generate_visualisations(data):
    # Visualisation 1: Histogramme
    fig, ax = plt.subplots()
    sns.histplot(data["column1"], binwidth=1)
    ax.set_title("Histogramme de la colonne 1")
    ax.set_xlabel("Valeur")
    ax.set_ylabel("Fréquence")
    st.pyplot(fig)

    # Visualisation 2: Graphique à barres
    fig, ax = plt.subplots()
    sns.barplot(x="column2", y="column3", data=data)
    ax.set_title("Graphique à barres de la colonne 2 et 3")
    ax.set_xlabel("Valeur de la colonne 2")
    ax.set_ylabel("Valeur de la colonne 3")
    st.pyplot(fig)

# Fonction pour traiter les erreurs
def traitement_erreur():
    try:
        data = load_data()
        generate_visualisations(data)
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")

# Application Streamlit
def main():
    st.title("Dashboard Streamlit")
    st.write("Bienvenue dans notre dashboard interactif !")

    # Menu déroulant pour choisir les colonnes
    options = data.columns.tolist()
    selected_columns = st.multiselect("Choisissez les colonnes à visualiser", options)

    # Traitement des erreurs
    try:
        data = load_data()
        if selected_columns:
            generate_visualisations(data[selected_columns])
        else:
            st.write("Veuillez sélectionner des colonnes pour générer une visualisation.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {str(e)}")

# Exécution de l'application
if __name__ == "__main__":
    main()
