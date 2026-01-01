python
# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from PIL import Image

# FONCTIONNALITÉ PRINCIPALE

def fonctionnalite_principale():
    try:
        # CHARGEMENT DES DONNÉES
        @st.cache
        def ChargerDonnes():
            data_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
            donneres = pd.read_csv(data_url)
            return donneres

        donneres = ChargerDonnes()

        # TRAITEMENT ET ANALYSE
        donneuréséle = donneres[['total_bill','tip']]

        correlation = donneuréséle.corr()
        corr_matrix = correlation.to_html()

        st.markdown(f"**CORR ÉLÉMENT DE CORRÉLATION ENTRE TOTAL BILL ET TIPE**")
        st.write(corr_matrix)

        st.markdown('\n')

        # PREMIÈRE QUESTION - Corr à l'aide de seaborn 

        import seaborn as sns

        f, ax = plt.subplots(figsize=(10, 8))
        heatmap = sns.heatmap(donneuréséle.corr(),annot=True,cmap='coolwarm',ax=ax,annot_kws={"fontsize":7}).figure()
        st.pyplot(heatmap)

        st.image(Image.open("logo.jpg"))

    except Exception as e:
        st.markdown(f"**UNE ERREUR EST ARRIVERE**")
        st.write(e)

def main():
    st.title("Fonctionnalité principale")
    
    if 'run' not in st.session_state:
        st.session_state.run = False
    cols = st.columns(2)

    if cols[0].button("Lancer la première étape"):
        st.session_state.run = True
    
    if  st.session_state.run:
        fonctionnalite_principale()
    
    if cols[1].button("Réinitialiser"):
        st.session_state.run = False
        
if __name__ == "__main__":
    main()
