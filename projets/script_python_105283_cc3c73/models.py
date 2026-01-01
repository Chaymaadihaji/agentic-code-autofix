python
# models.py

from typing import List
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DataScienceModel:
    def __init__(self, data: pd.DataFrame):
        """
        Initialisation du modèle.

        Args:
            data (pd.DataFrame): Données d'entrée.

        Raises:
            ValueError: Si les données sont vides.
        """
        if not data.empty:
            self.data = data
        else:
            raise ValueError("Données vides")

    def preprocess_data(self) -> pd.DataFrame:
        """
        Prétraitement des données.

        Returns:
            pd.DataFrame: Données prétraitées.
        """
        try:
            # Créer des variables numériques
            self.data['var_num_1'] = np.random.rand(len(self.data))
            self.data['var_num_2'] = np.random.rand(len(self.data))

            # Transformer les chaînes en numériques
            self.data['var_str'] = self.data['var_str'].astype('category')
            self.data['var_str'] = self.data['var_str'].cat.codes

            return self.data
        except Exception as e:
            print(f"Erreur : {e}")
            return pd.DataFrame()

    def train_model(self) -> LogisticRegression:
        """
        Formation du modèle.

        Returns:
            LogisticRegression: Modèle formé.
        """
        try:
            # Séparation des données en entraînement et test
            X_train, X_test, y_train, y_test = train_test_split(self.data[['var_num_1', 'var_num_2']], self.data['var_target'], test_size=0.2, random_state=42)

            # Créer un modèle de régression logistique
            model = LogisticRegression(max_iter=1000)

            # Entraîner le modèle
            model.fit(X_train, y_train)

            return model
        except Exception as e:
            print(f"Erreur : {e}")
            return None

    def evaluate_model(self, model: LogisticRegression) -> None:
        """
        Évaluation du modèle.

        Args:
            model (LogisticRegression): Modèle à évaluer.
        """
        try:
            # Prédre les valeurs pour les données de test
            y_pred = model.predict(X_test)

            # Évaluer la précision du modèle
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Précision : {accuracy:.2f}")
        except Exception as e:
            print(f"Erreur : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Simuler des données
    df = pd.DataFrame({
        'var_str': ['A', 'B', 'A', 'C', 'B'],
        'var_target': [1, 0, 1, 1, 0]
    })

    # Créer un modèle
    model = DataScienceModel(df)

    # Prétraiter les données
    df_preprocessed = model.preprocess_data()

    # Former le modèle
    logistic_regression = model.train_model()

    # Évaluer le modèle
    model.evaluate_model(logistic_regression)
