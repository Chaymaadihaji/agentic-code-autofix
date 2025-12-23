# data_processor.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Génération de données pour le dashboard
@st.cache
def generer_donnees():
    donnees = {
        "Nom": ["John", "Anna", "Peter", "Linda", "Bart", "Mia"],
        "Âge": [28, 24, 35, 32, 40, 22],
        "Salaire": [50000, 60000, 70000, 80000, 90000, 40000]
    }
    df = pd.DataFrame(donnees)
    return df

# Calcul des statistiques/métriques
def calcul_statistiques(df):
    statistiques = {
        "Moyenne âge": df["Âge"].mean(),
        "Moyenne salaire": df["Salaire"].mean(),
        "Nombre d'employés": len(df)
    }
    return statistiques

# API pour les données en temps réel
def api_donnees_en_temps_reel():
    df = generer_donnees()
    return df

# Structure modulaire pour différentes visualisations
def visualisation(df):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    
    sns.scatterplot(ax=axes[0], x="Âge", y="Salaire", data=df)
    axes[0].set_title("Salaire en fonction de l'âge")
    
    sns.barplot(ax=axes[1], x="Nom", y="Salaire", data=df)
    axes[1].set_title("Salaire par employé")
    
    st.pyplot(fig)

# Filtres pour les données
def filtres(df):
    nom = st.selectbox("Sélectionnez un employé", df["Nom"])
    df_filtré = df[df["Nom"] == nom]
    return df_filtré

# Chargement de données CSV
def charger_donnees_csv():
    fichier_csv = st.file_uploader("Charger un fichier CSV", type=["csv"])
    if fichier_csv:
        df = pd.read_csv(fichier_csv)
        return df

# Statistiques
def statistiques():
    df = generer_donnees()
    statistiques = calcul_statistiques(df)
    st.write("Statistiques:")
    st.write(f"Moyenne âge: {statistiques['Moyenne âge']}")
    st.write(f"Moyenne salaire: {statistiques['Moyenne salaire']}")
    st.write(f"Nombre d'employés: {statistiques['Nombre d'employés']}")

# Main
if __name__ == "__main__":
    st.title("Dashboard")
    st.write("Bienvenue sur le dashboard!")
    
    # Chargement de données CSV
    df_csv = charger_donnees_csv()
    
    # Génération de données si aucune données CSV n'est chargée
    if not df_csv:
        df = generer_donnees()
    else:
        df = df_csv
    
    # Visualisation
    visualisation(df)
    
    # Filtres
    df_filtré = filtres(df)
    
    # Statistiques
    statistiques()
