import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données CSV
@st.cache
def load_data(file):
    return pd.read_csv(file)

# Affichage des graphiques interactifs
def affiche_graphiques(data):
    st.subheader("Graphiques")
    fig, ax = plt.subplots()
    data['column1'].plot(kind='line', ax=ax)
    st.pyplot(fig)

# Filtres pour les données
def filtres(data):
    st.subheader("Filtres")
    categorie = st.selectbox("Sélectionner une catégorie", data['column1'].unique())
    filtered_data = data[data['column1'] == categorie]
    return filtered_data

# Calcul de statistiques
def statistiques(data):
    st.subheader("Statistiques")
    moyenne = data['column1'].mean()
    mediane = data['column1'].median()
    st.write(f"Moyenne : {moyenne}")
    st.write(f"Mediane : {mediane}")

# Tableau de données
def tableau(data):
    st.subheader("Tableau de données")
    st.write(data.head())

# Fonction principale
def main():
    st.title("Analyse de données CSV")
    file = "donnees.csv"
    data = load_data(file)
    st.write(data.head())
    affiche_graphiques(data)
    filtered_data = filtres(data)
    tableau(filtered_data)
    statistiques(data)

if __name__ == "__main__":
    main()
