# app.py

from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap
from forms import Formulaire
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

# Données en mémoire
donnees = [
    {"nom": "John", "age": 25, "ville": "Paris"},
    {"nom": "Jane", "age": 30, "ville": "Lyon"},
    {"nom": "Bob", "age": 35, "ville": "Marseille"}
]

# Route index
@app.route("/")
def index():
    return render_template("index.html")

# Route pour afficher les données
@app.route("/donnees", methods=["GET"])
def donnees_route():
    return jsonify(donnees)

# Route pour afficher les graphiques
@app.route("/graphiques", methods=["GET"])
def graphiques_route():
    return render_template("graphiques.html")

# Route pour afficher les formulaires
@app.route("/formulaire", methods=["GET", "POST"])
def formulaire_route():
    form = Formulaire()
    if form.validate_on_submit():
        nom = form.nom.data
        age = form.age.data
        ville = form.ville.data
        donnees.append({"nom": nom, "age": age, "ville": ville})
    return render_template("formulaire.html", form=form)

# Route pour afficher les cartes
@app.route("/cartes", methods=["GET"])
def cartes_route():
    return render_template("cartes.html")

# Route pour afficher les tableaux
@app.route("/tableaux", methods=["GET"])
def tableaux_route():
    return render_template("tableaux.html")

# Route pour afficher les galerie
@app.route("/galerie", methods=["GET"])
def galerie_route():
    return render_template("galerie.html")

# Route pour afficher les données en temps réel
@app.route("/temps_reel", methods=["GET"])
def temps_reel_route():
    return render_template("temps_reel.html", donnees=donnees)

# Route pour les graphiques interactifs
@app.route("/graphiques_interactifs", methods=["GET"])
def graphiques_interactifs_route():
    return render_template("graphiques_interactifs.html")

# Route pour le filtrage et le tri des données
@app.route("/filtrer_et_tri", methods=["GET"])
def filtrer_et_tri_route():
    return render_template("filtrer_et_tri.html")

# Gestion des erreurs
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
