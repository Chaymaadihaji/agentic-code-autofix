import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données CSV
@st.cache
def load_data(file):
    return pd.read_csv(file)

# Fonction pour calculer les statistiques
def calc_stats(data):
    return {
        'min': data.min().min(),
        'max': data.max().max(),
        'mean': data.mean().mean(),
        'median': data.median().median()
    }

# Fonction pour afficher les graphiques
def show_graphs(data):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
    sns.scatterplot(data=data, x='A', y='B', ax=axes[0, 0])
    sns.lineplot(data=data, x='A', y='B', ax=axes[0, 1])
    sns.barplot(data=data, x='A', y='B', ax=axes[1, 0])
    sns.boxplot(data=data, x='A', y='B', ax=axes[1, 1])
    st.pyplot(fig)

# Fonction pour afficher les filtres
def show_filters(data):
    st.write("Choisissez vos filtres:")
    col1, col2 = st.columns(2)
    min_val = col1.slider("Min", min_value=data.min().min(), max_value=data.max().max(), value=data.min().min())
    max_val = col2.slider("Max", min_value=data.min().min(), max_value=data.max().max(), value=data.max().max())
    return min_val, max_val

# Fonction pour afficher les statistiques
def show_stats(stats):
    st.write("Statistiques:")
    st.write(f"Min: {stats['min']}")
    st.write(f"Max: {stats['max']}")
    st.write(f"Mean: {stats['mean']}")
    st.write(f"Median: {stats['median']}")

# Fonction pour afficher la table
def show_table(data):
    st.write(data)

# Fonction pour afficher le dashboard
def show_dashboard():
    st.title("Dashboard")
    file = "data.csv"
    data = load_data(file)
    st.write("Données:")
    st.write(data)
    st.write("Graphiques:")
    show_graphs(data)
    min_val, max_val = show_filters(data)
    filtered_data = data[(data['A'] >= min_val) & (data['A'] <= max_val)]
    st.write("Données filtrées:")
    st.write(filtered_data)
    stats = calc_stats(filtered_data)
    show_stats(stats)
    show_table(filtered_data)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    show_dashboard()
