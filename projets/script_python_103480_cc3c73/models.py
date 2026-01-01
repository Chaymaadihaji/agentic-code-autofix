python
# models.py
# Import des bibliothèques nécessaires
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.exceptions import NotFittedError

class ModeleDeClasse:
    """Classe pour créer et entraîner un modèle de classification"""
    
    def __init__(self, x: pd.DataFrame, y: pd.Series):
        """Initialisation du modèle"""
        
        self.x = x
        self.y = y
        self.model = None

    def diviser_les_donnees(self):
        """Diviser les données en train et test"""
        
        try:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.2, random_state=42)
            return self.x_train, self.x_test, self.y_train, self.y_test
        except ValueError as e:
            print(f"Erreur lors de la division des données : {e}")
            raise

    def entraîner_le_model(self):
        """Entraîner le modèle de classification"""
        
        try:
            self.model = LogisticRegression()
            self.model.fit(self.x_train, self.y_train)
            return self.model
        except NotFittedError as e:
            print(f"Le modèle doit être entraîné avant de faire une prédiction : {e}")
            raise

    def faire_predict(self):
        """Faire des prédictions avec le modèle"""
        
        try:
            if self.model is None:
                raise NotFittedError("Le modèle doit être entraîné avant de faire une prédiction")
            self.y_pred = self.model.predict(self.x_test)
            return self.y_pred
        except NotFittedError as e:
            print(f"Erreur lors de la prédiction : {e}")
            raise

    def évaluer_le_model(self):
        """Évaluer la performance du modèle"""
        
        try:
            self.y_pred = self faire_predict()
            self.score = accuracy_score(self.y_test, self.y_pred)
            return self.score
        except Exception as e:
            print(f"Erreur lors de l'évaluation du modèle : {e}")
            raise

# Créer un exemple de données
if __name__ == "__main__":
    # Import des données
    from sklearn.datasets import load_iris
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target

    # Créer un objet de la classe ModeleDeClasse
    modele = ModeleDeClasse(df, df['target'])

    # Diviser les données en train et test
    x_train, x_test, y_train, y_test = modele.diviser_les_donnees()

    # Entraîner le modèle
    modele.entraîner_le_model()

    # Faire des prédictions
    y_pred = modele.faire_predict()

    # Évaluer la performance du modèle
    score = modele.évaluer_le_model()
    print(f"Score du modèle : {score}")
