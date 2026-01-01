import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Calculatrice et gestion de données")

# Calculatrice
st.subheader("Calculatrice")
calc = st.number_input("Nombre 1", 0.0)
calc2 = st.number_input("Nombre 2", 0.0)
bouton = st.button("Calculer")
if bouton:
    result = calc + calc2
    st.write("Résultat:", result)

# Formulaires
st.subheader("Formulaires")
nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
submit = st.button("Soumettre")
if submit:
    st.write("Bonjour, ", nom, " ", prenom)

# Tableaux
st.subheader("Tableaux")
data = {"Nom": ["John", "Mary", "David"], "Âge": [25, 31, 42]}
df = pd.DataFrame(data)
st.write(df)

# Graphiques
st.subheader("Graphiques")
x = [1, 2, 3]
y = [2, 4, 6]
plt.plot(x, y)
st.pyplot()

# Dashboard
st.subheader("Dashboard")
st.write("Bienvenue sur le dashboard")

# Filtres
st.subheader("Filtres")
filtre = st.selectbox("Filtrer par", ["Tout", "Nom", "Prénom"])
if filtre == "Nom":
    st.write("Filtrer par nom")
elif filtre == "Prénom":
    st.write("Filtrer par prénom")
