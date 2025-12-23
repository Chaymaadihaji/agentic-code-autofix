# Importation du module Flask
from flask import Flask

# Création d'une instance de l'application Flask
app = Flask(__name__)

# Définition d'une route pour la page d'accueil
@app.route('/')
def accueil():
    # Retourne un message de bienvenue
    return 'Bonjour le monde !'

# Exécution de l'application si le script est lancé directement
if __name__ == "__main__":
    # Lancement de l'application en mode debug
    app.run(debug=True)