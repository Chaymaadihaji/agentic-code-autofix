import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# Chargement des données
with open('donnees.json') as f:
    donnees = json.load(f)

# Fonction pour créer un formulaire
def creer_formulaire():
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    return nom, prenom

# Fonction pour afficher les données
def afficher_donnees():
    st.header("Données")
    st.write(pd.DataFrame(donnees))

# Fonction pour afficher les graphiques
def afficher_graphiques():
    st.header("Graphiques")
    fig, ax = plt.subplots()
    ax.bar(donnees['nom'], donnees['valeur'])
    st.pyplot(fig)

# Fonction pour créer un dashboard
def creer_dashboard():
    st.header("Dashboard")
    st.write("Bienvenue sur notre dashboard")
    nom, prenom = creer_formulaire()
    st.write(f"Bonjour {nom} {prenom}!")

# Fonction pour créer des filtres
def creer_filtres():
    st.header("Filtres")
    categorie = st.selectbox("Catégorie", ["A", "B", "C"])
    st.write(f"Vous avez sélectionné la catégorie {categorie}")

# Fonction pour gérer les entrées/sorties
def gérer_entrees_sorties():
    if st.button("Sauvegarder"):
        with open('donnees.json', 'w') as f:
            json.dump({'nom': st.session_state.nom, 'prenom': st.session_state.prenom}, f)

# Fonction pour créer l'interface
def creer_interface():
    st.title("Application Streamlit")
    st.header("Formulaire")
    creer_formulaire()
    st.header("Données")
    afficher_donnees()
    st.header("Graphiques")
    afficher_graphiques()
    st.header("Dashboard")
    creer_dashboard()
    st.header("Filtres")
    creer_filtres()
    st.header("Gestion des entrées/sorties")
    gérer_entrees_sorties()

# Fonction pour lancer l'application
def lancer_application():
    if 'nom' not in st.session_state:
        st.session_state.nom = 'Inconnu'
    if 'prenom' not in st.session_state:
        st.session_state.prenom = 'Inconnu'
    creer_interface()

# Lancement de l'application
if __name__ == "__main__":
    lancer_application()
