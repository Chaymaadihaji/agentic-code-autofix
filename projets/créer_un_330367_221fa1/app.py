import json
import random
from flask import Flask, render_template, request
from flask_bootstrap4 import Bootstrap
from collections import Counter

app = Flask(__name__)
Bootstrap(app)

# Données de démonstration
donnees = [
    {"id": 1, "nom": "Tâche 1", "état": "en cours"},
    {"id": 2, "nom": "Tâche 2", "état": "terminée"},
    {"id": 3, "nom": "Tâche 3", "état": "en cours"},
    {"id": 4, "nom": "Tâche 4", "état": "terminée"},
    {"id": 5, "nom": "Tâche 5", "état": "en cours"}
]

# API pour les données en temps réel
@app.route("/api/taches", methods=["GET"])
def get_taches():
    return json.dumps(donnees)

# Route pour la page de dashboard
@app.route("/")
def index():
    return render_template("index.html", taches=donnees)

# Route pour la page de création de tâche
@app.route("/create", methods=["GET", "POST"])
def create_tache():
    if request.method == "POST":
        nom = request.form["nom"]
        etat = request.form["etat"]
        donnees.append({"id": len(donnees) + 1, "nom": nom, "état": etat})
        return "Tâche créée avec succès"
    return render_template("create.html")

# Route pour la page de statistiques
@app.route("/statistiques")
def statistiques():
    etats = [tache["état"] for tache in donnees]
    comptes = Counter(etats)
    return render_template("statistiques.html", comptes=comptes)

# Route pour la page de filtrage
@app.route("/filtrer", methods=["GET", "POST"])
def filtrer():
    if request.method == "POST":
        etat = request.form["etat"]
        donnees_filtrees = [tache for tache in donnees if tache["état"] == etat]
        return render_template("filtrer.html", taches=donnees_filtrees)
    return render_template("filtrer.html")

# Route pour la page de tri
@app.route("/tri", methods=["GET", "POST"])
def tri():
    if request.method == "POST":
        ordre = request.form["ordre"]
        if ordre == "nom":
            donnees.sort(key=lambda tache: tache["nom"])
        elif ordre == "état":
            donnees.sort(key=lambda tache: tache["état"])
        return render_template("tri.html", taches=donnees)
    return render_template("tri.html")

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
