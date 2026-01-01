import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# Fonctions
def calculatrice():
    num1 = st.number_input("Nombre 1")
    op = st.selectbox("Opération", ["+", "-", "*", "/"])
    num2 = st.number_input("Nombre 2")
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        return num1 / num2

def formulaire():
    nom = st.text_input("Nom")
    age = st.number_input("Âge")
    return nom, age

def tableau():
    df = pd.DataFrame({
        "Nom": ["Jean", "Marie", "Pierre"],
        "Âge": [25, 31, 42]
    })
    return df

def graphique():
    x = [1, 2, 3]
    y = [2, 4, 6]
    plt.plot(x, y)
    return plt

def filtrage():
    return {"filtré": True}

def affichage_donnees():
    st.title("Affichage de données")
    df = tableau()
    st.write(df)

def graphiques_interactifs():
    st.title("Graphiques interactifs")
    graphique().show()

def filtrage_donnees():
    st.title("Filtrage de données")
    filtrage = filtrage()
    st.write(filtrage)

# Routes
if __name__ == "__main__":
    st.title("Application")
    menu = ["Calculatrice", "Formulaire", "Tableau", "Graphique", "Filtrage"]
    choice = st.selectbox("Menu", menu)
    if choice == "Calculatrice":
        st.title("Calculatrice")
        st.write(calculatrice())
    elif choice == "Formulaire":
        st.title("Formulaire")
        nom, age = formulaire()
        st.write(f"Nom: {nom}, Âge: {age}")
    elif choice == "Tableau":
        st.title("Tableau")
        affichage_donnees()
    elif choice == "Graphique":
        st.title("Graphique")
        graphiques_interactifs()
    elif choice == "Filtrage":
        st.title("Filtrage")
        filtrage_donnees()
