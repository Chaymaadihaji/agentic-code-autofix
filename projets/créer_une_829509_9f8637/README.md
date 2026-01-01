import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Création de la calculatrice
def calculatrice():
    num1 = st.number_input("Nombre 1")
    num2 = st.number_input("Nombre 2")
    op = st.selectbox("Opération", ["+", "-", "*", "/"])
    if st.button("Calculer"):
        if op == "+":
            st.write(num1 + num2)
        elif op == "-":
            st.write(num1 - num2)
        elif op == "*":
            st.write(num1 * num2)
        elif op == "/":
            if num2 != 0:
                st.write(num1 / num2)
            else:
                st.error("Erreur : Division par zéro")

# Création du formulaire
def formulaire():
    nom = st.text_input("Nom")
    age = st.number_input("Âge")
    st.write("Bonjour, " + nom + " ! Tu as " + str(age) + " ans.")

# Création du tableau
def tableau():
    df = pd.DataFrame({
        "Nom": ["Pierre", "Paul", "Jacques"],
        "Âge": [25, 30, 35]
    })
    st.write(df)

# Création du graphique
def graphique():
    sns.set()
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Nom", y="Âge", data=pd.DataFrame({
        "Nom": ["Pierre", "Paul", "Jacques"],
        "Âge": [25, 30, 35]
    }))
    st.pyplot()

# Création du dashboard
def dashboard():
    st.write("Informations clés")
    st.write("Nombre de visiteurs : 100")
    st.write("Nombre de clicks : 500")

# Création du filtre
def filtre():
    data = pd.DataFrame({
        "Nom": ["Pierre", "Paul", "Jacques"],
        "Âge": [25, 30, 35]
    })
    age_min = st.number_input("Âge minimum")
    age_max = st.number_input("Âge maximum")
    st.write(data[(data["Âge"] >= age_min) & (data["Âge"] <= age_max)])

# Chemin d'accès
if __name__ == "__main__":
    # Menu
    menu = ["Calculatrice", "Formulaire", "Tableau", "Graphique", "Dashboard", "Filtre"]
    choice = st.selectbox("Choisissez une option", menu)

    # Affichage des composants
    if choice == "Calculatrice":
        calculatrice()
    elif choice == "Formulaire":
        formulaire()
    elif choice == "Tableau":
        tableau()
    elif choice == "Graphique":
        graphique()
    elif choice == "Dashboard":
        dashboard()
    elif choice == "Filtre":
        filtre()
