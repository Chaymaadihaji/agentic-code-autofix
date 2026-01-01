import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# Gestion des entrées/sorties
st.title("Application Streamlit")

# Fonction pour afficher les données
def afficher_donnes():
    # Données en mémoire
    data = {
        "Nom": ["John", "Anna", "Peter", "Linda"],
        "Âge": [28, 24, 35, 32],
        "Villes": ["New York", "Paris", "Tokyo", "Londres"]
    }

    # Créer un dataframe
    df = pd.DataFrame(data)

    # Afficher le dataframe
    st.write(df)

# Fonction pour afficher des graphiques interactifs
def afficher_graphique():
    # Données en mémoire
    data = {
        "Nom": ["John", "Anna", "Peter", "Linda"],
        "Âge": [28, 24, 35, 32]
    }

    # Créer un dataframe
    df = pd.DataFrame(data)

    # Afficher un graphique
    fig, ax = plt.subplots()
    ax.bar(df["Nom"], df["Âge"])
    st.pyplot(fig)

# Fonction pour filtrer les données
def filtrer_donnes():
    # Données en mémoire
    data = {
        "Nom": ["John", "Anna", "Peter", "Linda"],
        "Âge": [28, 24, 35, 32],
        "Villes": ["New York", "Paris", "Tokyo", "Londres"]
    }

    # Créer un dataframe
    df = pd.DataFrame(data)

    # Filtre les données
    filtre_age = st.slider("Âge", 0, 40, (20, 30))
    filtre_ville = st.selectbox("Ville", df["Villes"].unique())

    # Afficher les données filtrées
    st.write(df[(df["Âge"] >= filtre_age[0]) & (df["Âge"] <= filtre_age[1]) & (df["Villes"] == filtre_ville)])

# Créer une calculatrice
def calculatrice():
    num1 = st.number_input("Premier nombre")
    op = st.selectbox("Opération", ["+", "-", "*", "/"])
    num2 = st.number_input("Deuxième nombre")

    if op == "+":
        st.write("Résultat:", num1 + num2)
    elif op == "-":
        st.write("Résultat:", num1 - num2)
    elif op == "*":
        st.write("Résultat:", num1 * num2)
    elif op == "/":
        if num2 != 0:
            st.write("Résultat:", num1 / num2)
        else:
            st.error("Division par zéro!")

# Créer un formulaire
def formulaire():
    nom = st.text_input("Nom")
    age = st.number_input("Âge")

    if st.button("Soumettre"):
        st.write("Bonjour, ", nom, "! Vous avez", age, "ans.")

# Créer un tableau
def tableau():
    data = {
        "Nom": ["John", "Anna", "Peter", "Linda"],
        "Âge": [28, 24, 35, 32]
    }

    # Créer un dataframe
    df = pd.DataFrame(data)

    # Afficher le dataframe
    st.write(df)

# Créer un graphique
def graphique():
    # Données en mémoire
    data = {
        "Nom": ["John", "Anna", "Peter", "Linda"],
        "Âge": [28, 24, 35, 32]
    }

    # Créer un dataframe
    df = pd.DataFrame(data)

    # Afficher un graphique
    fig, ax = plt.subplots()
    ax.bar(df["Nom"], df["Âge"])
    st.pyplot(fig)

# Créer un filtre
def filtre():
    data = {
        "Nom": ["John", "Anna", "Peter", "Linda"],
        "Âge": [28, 24, 35, 32],
        "Villes": ["New York", "Paris", "Tokyo", "Londres"]
    }

    # Créer un dataframe
    df = pd.DataFrame(data)

    # Filtre les données
    filtre_age = st.slider("Âge", 0, 40, (20, 30))
    filtre_ville = st.selectbox("Ville", df["Villes"].unique())

    # Afficher les données filtrées
    st.write(df[(df["Âge"] >= filtre_age[0]) & (df["Âge"] <= filtre_age[1]) & (df["Villes"] == filtre_ville)])

# Créer un dashboard
def dashboard():
    afficher_donnes()
    afficher_graphique()
    formulaire()
    tableau()
    graphique()
    filtre()

# Lancement de l'app
if __name__ == "__main__":
    st.sidebar.title("Menu")
    option = st.sidebar.selectbox("Choisissez une option", ["Calculatrice", "Formulaire", "Tableau", "Graphique", "Filtre", "Dashboard"])

    if option == "Calculatrice":
        calculatrice()
    elif option == "Formulaire":
        formulaire()
    elif option == "Tableau":
        tableau()
    elif option == "Graphique":
        graphique()
    elif option == "Filtre":
        filtre()
    elif option == "Dashboard":
        dashboard()
