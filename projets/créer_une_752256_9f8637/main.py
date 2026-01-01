# main.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Données en mémoire
donnees = [
    {"nom": "John", "âge": 25},
    {"nom": "Jane", "âge": 30},
    {"nom": "Bob", "âge": 35},
]

# Fonction pour le filtrage et le tri
def filtrer_donnees(filtre, tri):
    global donnees
    if filtre:
        donnees = [donnee for donnee in donnees if filtre in str(donnee).lower()]
    if tri:
        if tri == "asc":
            donnees.sort(key=lambda x: x["âge"])
        elif tri == "desc":
            donnees.sort(key=lambda x: x["âge"], reverse=True)

# Route pour l'affichage de données en temps réel
@app.route("/")
def index():
    return render_template("index.html")

# Route pour les graphiques interactifs
@app.route("/graphiques")
def graphiques():
    return render_template("graphiques.html")

# Route pour le filtrage et le tri des données
@app.route("/filtrer", methods=["POST"])
def filtrer():
    filtre = request.form["filtre"]
    tri = request.form["tri"]
    filtrer_donnees(filtre, tri)
    return jsonify(donnees)

# Route pour le lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
