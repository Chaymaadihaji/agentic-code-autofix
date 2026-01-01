import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Calculatrice et outils de gestion de données")

# Calculatrice
num1 = st.number_input("Entrer le premier nombre")
num2 = st.number_input("Entrer le deuxième nombre")
operateur = st.selectbox("Sélectionner l'opérateur", ["+", "-", "*", "/"])
resultat = st.button("Calculer")

if resultat:
    if operateur == "+":
        st.write(num1 + num2)
    elif operateur == "-":
        st.write(num1 - num2)
    elif operateur == "*":
        st.write(num1 * num2)
    elif operateur == "/":
        if num2 != 0:
            st.write(num1 / num2)
        else:
            st.error("Erreur : division par zéro")

# Formulaires
st.header("Formulaires")
nom = st.text_input("Entrer le nom")
prenom = st.text_input("Entrer le prénom")
age = st.number_input("Entrer l'âge")
submit = st.button("Soumettre")

if submit:
    st.write(f"Bonjour {nom} {prenom}, vous avez {age} ans")

# Tableaux
st.header("Tableaux")
df = pd.DataFrame({
    "Nom": ["Pierre", "Paul", "Jacques"],
    "Prénom": ["Dupont", "Dumas", "Durand"],
    "Âge": [25, 30, 35]
})
st.write(df)

# Graphiques
st.header("Graphiques")
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [5, 7, 10])
st.pyplot(fig)

# Dashboard
st.header("Dashboard")
st.write("Voici le dashboard")

# Filtres
st.header("Filtres")
filtre_nom = st.selectbox("Sélectionner le nom", ["Pierre", "Paul", "Jacques"])
filtre_age = st.slider("Sélectionner l'âge", 18, 65)

# Afficher les données filtrées
st.write(f"Nom : {filtre_nom}, Âge : {filtre_age}")
