import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dash
import plotly.express as px

def afficher_donnes(df):
    st.title("Données")
    st.write(df)

def graphique_interactif(df, column1, column2):
    st.title("Graphique interactif")
    fig = px.scatter(df, x=column1, y=column2)
    st.plotly_chart(fig)

def filtrer_donnes(df, column, valeur):
    st.title("Filtrer données")
    filtered_df = df[df[column] == valeur]
    return filtered_df

def calculatrice():
    st.title("Calculatrice")
    num1 = st.number_input("Entrer le premier nombre")
    num2 = st.number_input("Entrer le deuxième nombre")
    operateur = st.selectbox("Sélectionner l'opérateur", ["+", "-", "*", "/"])
    if st.button("Calculer"):
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
                st.write("Erreur : division par zéro")

def main():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [2, 3, 5, 7, 11]
    })
    
    calculatrice()
    afficher_donnes(df)
    graphique_interactif(df, "A", "B")
    filtered_df = filtrer_donnes(df, "A", 3)
    afficher_donnes(filtered_df)

if __name__ == "__main__":
    st.title("Application Streamlit")
    main()
