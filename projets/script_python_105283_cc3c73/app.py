python
# app.py
"""
Application web servant d'exemple pour les fonctionnalités de data science
"""

import os
from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)

def charge_data(nom_fichier):
    """
    Charge les données depuis le fichier spécifié
    
    Args:
        nom_fichier (str): Chemin vers le fichier de données
    
    Returns:
        pd.DataFrame: Données chargées
    """
    try:
        données = pd.read_csv(nom_fichier)
        return données
    except Exception as e:
        return f"Erreur lors du chargement des données : {e}"

def créer_modele_entraîné(data, target):
    """
    Crée un modèle de reconnaissance de données à partir des données et du target
    
    Args:
        data (pd.DataFrame): Données de features
        target (pd.Series): Label de classification
    
    Returns:
        RandomForestClassifier: Modèle entraîné
    """
    try:
        données_entraînement, données_test, labels_entraînement, labels_test = train_test_split(data, target, test_size=0.2, random_state=42)
        modèle = RandomForestClassifier(n_estimators=100, random_state=42)
        modèle.fit(données_entraînement, labels_entraînement)
        return modèle
    except Exception as e:
        return f"Erreur lors de l'entraînement du modèle : {e}"

def prédire_sorties(mdl, données):
    """
    Prédit les sorties pour les données d'entrée
    
    Args:
        mdl (RandomForestClassifier): Modèle entraîné
        données (pd.DataFrame): Données d'entrée
    
    Returns:
        list: Prédictions des sorties
    """
    try:
        prédictions = mdl.predict(données)
        return prédictions
    except Exception as e:
        return f"Erreur lors de la prédiction des sorties : {e}"

@app.route('/', methods=['GET', 'POST'])
def fonctionnalite_principale():
    """
    Fonctionnalité principale de l'application : chargement et utilisation des données
    """
    if request.method == 'POST':
        # Chargement des données
        nom_fichier = request.form.get('fichier')
        données = charge_data(nom_fichier)
        
        # Prétraitement des données
        données = données.dropna()
        données = données.astype({'feature1': 'float64', 'feature2': 'int64'})
        
        # Classification
        target = données['target']
        data = données.drop(columns=['target'])
        mdl = créer_modele_entraîné(data, target)
        
        # Prédiction
        prédictions = prédiction_sorties(mdl, data)
        
        # Affichage résultat
        rendu = render_template('resultat.html', resultats=prédictions)
        return rendu
    
    # Interface utilisateur
    rendu = render_template('index.html')
    return rendu

if __name__ == '__main__':
    app.run(debug=True, port=5000)
