import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard")

# Upload CSV
st.sidebar.header("📁 Import des données")
uploaded_file = st.sidebar.file_uploader("Choisir un fichier CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # KPI
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Chiffre d'affaires", f"${df['Prix'].sum() * df['Quantité'].sum():,.0f}")
    with col2:
        st.metric("Ventes totales", f"{df['Quantité'].sum():,.0f}")
    with col3:
        st.metric("Produits", f"{df['Produit'].nunique()}")
    
    # Graphiques
    st.subheader("📈 Graphiques")
    fig = px.line(df, x='Date', y='Prix', title='Évolution des prix')
    st.plotly_chart(fig)
    
    # Tableau
    st.subheader("📋 Données")
    st.dataframe(df)
    
    # Téléchargement
    csv = df.to_csv(index=False)
    st.download_button("📥 Télécharger CSV", csv, "ventes_filtrees.csv")
else:
    st.info("👆 Veuillez uploader un fichier CSV dans la sidebar")
