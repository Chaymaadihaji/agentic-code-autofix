python
# main.py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def fonctionnalite_principale():
    """
    Fonction principale du script de data science
    """
    try:
        # Chargement du dataset
        dataframe = pd.read_csv('donnees.csv')
        
        # Affichage des premières lignes du dataset
        print(dataframe.head())
        
        # Statistiques descriptives du dataset
        print(dataframe.describe())
        
        # Séparation des données en ensembles d'apprentissage et de test
        X = dataframe[['col1', 'col2']]  # Features
        y = dataframe['col3']  # Target
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Création d'un modèle de régression linéaire
        model = LinearRegression()
        
        # Apprentissage du modèle avec les données d'apprentissage
        model.fit(X_train, y_train)
        
        # Prédictions avec les données de test
        predictions = model.predict(X_test)
        
        # Évaluation du modèle
        score = model.score(X_test, y_test)
        mae = metrics.mean_absolute_error(y_test, predictions)
        mse = metrics.mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5
        
        print(f'MaE : {mae}, MSE : {mse}, RMSE : {rmse}, SCORE : {score}')
        
        # Affichage des résultats
        plt.scatter(predictions, y_test)
        plt.xlabel('Prédictions')
        plt.ylabel('Vraies valeurs')
        plt.show()
    
    except FileNotFoundError:
        print("Le fichier 'donnees.csv' n'a pas été trouvé.")
    except pd.errors.EmptyDataError:
        print("Le fichier 'donnees.csv' est vide.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == '__main__':
    fonctionnalite_principale()
