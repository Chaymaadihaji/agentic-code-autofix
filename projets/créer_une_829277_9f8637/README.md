import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
@st.cache
def charger_donnees():
    return pd.read_csv("donnees.csv")

# Fonction pour afficher les données
def afficher_donnees(donnees):
    st.write("Données")
    st.table(donnees)

# Fonction pour afficher les graphiques
def afficher_graphiques(donnees):
    st.write("Graphiques")
    plt.figure(figsize=(10,6))
    plt.plot(donnees["x"], donnees["y"])
    st.pyplot(plt.gcf())

# Fonction pour afficher les filtres
def afficher_filtres(donnees):
    st.write("Filtres")
    filtres = st.selectbox("Sélectionner un filtre", ["Tous", "Filtre 1", "Filtre 2"])
    if filtres == "Filtre 1":
        donnees = donnees[donnees["col1"] == "valeur1"]
    elif filtres == "Filtre 2":
        donnees = donnees[donnees["col2"] == "valeur2"]
    afficher_donnees(donnees)

# Fonction pour afficher le dashboard
def afficher_dashboard(donnees):
    st.write("Dashboard")
    st.metric("Total", donnees.shape[0])
    st.metric("Moyenne", donnees["col3"].mean())

# Fonction principale
def main():
    donnees = charger_donnees()
    st.title("Application Streamlit")
    st.sidebar.title("Menu")
    menu = st.sidebar.selectbox("Sélectionner un élément", ["Données", "Graphiques", "Filtres", "Dashboard"])
    if menu == "Données":
        afficher_donnees(donnees)
    elif menu == "Graphiques":
        afficher_graphiques(donnees)
    elif menu == "Filtres":
        afficher_filtres(donnees)
    elif menu == "Dashboard":
        afficher_dashboard(donnees)

if __name__ == "__main__":
    main()
