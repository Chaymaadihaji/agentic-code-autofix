import streamlit as st
import pandas as pd
import numpy as np
import json

# Chargement des données
with open('donnees.json') as f:
    donnees = json.load(f)

# Fonction de tri
def tri_data(data, colonne):
    return data.sort_values(colonne)

# Fonction de filtrage
def filtre_data(data, colonne, valeur):
    return data[data[colonne] == valeur]

# Fonction principal
def app():
    # Création de l'interface utilisateur
    st.title('Calculatrice')
    st.write('## Formulaire')
    
    # Formulaire
    nom = st.text_input('Nom')
    age = st.number_input('Âge', min_value=0)
    
    # Création du tableau
    df = pd.DataFrame(donnees)
    st.write('## Tableau')
    st.table(df)
    
    # Création du graphique
    st.write('## Graphique')
    st.line_chart(df['Valeur'])
    
    # Bouton pour lancer le tri
    if st.button('Tri'):
        colonne = st.selectbox('Colonne à trier', df.columns)
        tri = tri_data(df, colonne)
        st.write('## Tableau trié')
        st.table(tri)
    
    # Bouton pour lancer le filtrage
    if st.button('Filtrage'):
        colonne = st.selectbox('Colonne à filtrer', df.columns)
        valeur = st.selectbox('Valeur à filtrer', df[colonne].unique())
        filtre = filtre_data(df, colonne, valeur)
        st.write('## Tableau filtré')
        st.table(filtre)

# Lancement de l'app
if __name__ == "__main__":
    app()
