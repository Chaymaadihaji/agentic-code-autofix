# main.py
import requests
import json

# Configuration API OpenWeather
API_KEY = "votre_api_key_openweather"
BASE_URL = f"http://api.openweathermap.org/data/2.5/"

# Structure pour les données de ville
class Ville:
    def __init__(self, nom, lat, lon):
        self.nom = nom
        self.lat = lat
        self.lon = lon

# Structure pour les prévisions météo
class Prevision:
    def __init__(self, ville, jour, temp, conditions):
        self.ville = ville
        self.jour = jour
        self.temp = temp
        self.conditions = conditions

# Fonction pour récupérer les données de ville
def get_ville_data(ville):
    url = f"{BASE_URL}weather?q={ville.nom}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

# Fonction pour récupérer les prévisions météo
def get_previsions_data(ville):
    url = f"{BASE_URL}forecast?q={ville.nom}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

# Fonction pour gérer les alertes
def gestion_alertes(ville, previsions):
    for prevision in previsions:
        if prevision.temp < 0:
            return f"Alerte pour {ville.nom} : température inférieure à 0°C"

# Fonction pour gérer les favoris
def gestion_favoris(ville):
    return f"Ville ajoutée aux favoris : {ville.nom}"

# Fonction principale
def main():
    # Liste des villes
    villes = [
        Ville("Paris", 48.8566, 2.3522),
        Ville("Lyon", 45.7640, 4.8357),
        Ville("Marseille", 43.2965, 5.3698),
    ]

    # Récupération des données de ville
    for ville in villes:
        ville_data = get_ville_data(ville)
        print(f"Nom : {ville_data['name']} - Température : {ville_data['main']['temp']}°C")

        # Récupération des prévisions météo
        previsions_data = get_previsions_data(ville)
        previsions = []
        for prevision_data in previsions_data['list']:
            previsions.append(Prevision(ville, prevision_data['dt_txt'], prevision_data['main']['temp'], prevision_data['weather'][0]['description']))
        print("Prévisions :")
        for prevision in previsions:
            print(f"  - {prevision.jour} : {prevision.temp}°C - {prevision.conditions}")

        # Gestion des alertes
        alerte = gestion_alertes(ville, previsions)
        if alerte:
            print(alerte)

        # Gestion des favoris
        favori = gestion_favoris(ville)
        if favori:
            print(favori)

if __name__ == "__main__":
    main()
