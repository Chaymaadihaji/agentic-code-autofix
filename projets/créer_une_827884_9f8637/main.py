import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Application Streamlit", page_icon="🚀")

st.title("Application Streamlit Générée")
st.write("Demande: Créer une application Streamlit")
st.write("Tentative: 4/4")

st.sidebar.title("Menu")
option = st.sidebar.selectbox(
    "Choisir une fonctionnalité",
    ["Dashboard", "Données", "Graphiques", "À propos"]
)

if option == "Dashboard":
    st.header("Tableau de bord")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tentative", 4, f"+3")
    with col2:
        st.metric("Score", "95%", "5%")
    with col3:
        st.metric("Status", "Actif", "✓")
    
    data = pd.DataFrame({
        'x': range(1, 11),
        'y': np.random.randn(10)
    })
    st.line_chart(data)
    
elif option == "Données":
    st.header("Gestion des données")
    
    df = pd.DataFrame({
        'Nom': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Âge': [25, 30, 35, 28],
        'Ville': ['Paris', 'Lyon', 'Marseille', 'Toulouse'],
        'Score': [85, 92, 78, 88]
    })
    st.dataframe(df)
    
    age_filter = st.slider("Filtrer par âge", 20, 40, (25, 35))
    filtered_df = df[(df['Âge'] >= age_filter[0]) & (df['Âge'] <= age_filter[1])]
    st.write(f"Résultats filtrés: {len(filtered_df)}")
    st.dataframe(filtered_df)

elif option == "Graphiques":
    st.header("Visualisations")
    
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)
    
    hist_values = np.histogram(chart_data['A'], bins=20)[0]
    st.bar_chart(hist_values)
    
    scatter_data = pd.DataFrame({
        'x': np.random.randn(50),
        'y': np.random.randn(50)
    })
    st.scatter_chart(scatter_data)

else:
    st.header("À propos")
    st.write("""
    ## Application générée automatiquement
    
    Cette application Streamlit a été générée automatiquement
    par un robot développeur.
    
    **Détails:**
    - Type: streamlit
    - Tentative: 4/4
    - Date: Sat Dec 27 10:31:24 2025
    """)

if __name__ == "__main__":
    st.success("Application prête !")
