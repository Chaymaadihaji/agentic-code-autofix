import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Application Streamlit", page_icon="🚀")
st.title("Application Streamlit")
st.write("Demande : Créer une application Streamlit")

# Données d'exemple
data = pd.DataFrame({
    'Nom': ['Alice', 'Bob', 'Charlie'],
    'Âge': [25, 30, 35],
    'Ville': ['Paris', 'Lyon', 'Marseille']
})

st.dataframe(data)

# Graphique
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)

st.sidebar.title("Menu")
option = st.sidebar.selectbox("Choisir", ["Dashboard", "Données", "Graphiques"])
st.write(f"Option sélectionnée: {option}")