import os
from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import random
from statistics import mean

app = Flask(__name__)

# Génération de données pour le dashboard
donnees = [
    {"nom": "Tâche 1", "début": "2022-01-01", "fin": "2022-01-05", "état": "en cours"},
    {"nom": "Tâche 2", "début": "2022-02-01", "fin": "2022-02-10", "état": "terminée"},
    {"nom": "Tâche 3", "début": "2022-03-01", "fin": "2022-03-20", "état": "en cours"},
    {"nom": "Tâche 4", "début": "2022-04-01", "fin": "2022-04-15", "état": "terminée"},
    {"nom": "Tâche 5", "début": "2022-05-01", "fin": "2022-05-25", "état": "en cours"}
]

# Calcul des statistiques/métriques
def calcul_statistiques(donnees):
    temps_total = 0
    nb_taches_en_cours = 0
    nb_taches_terminées = 0
    for tache in donnees:
        temps_total += (datetime.strptime(tache["fin"], "%Y-%m-%d") - datetime.strptime(tache["début"], "%Y-%m-%d")).days
        if tache["état"] == "en cours":
            nb_taches_en_cours += 1
        elif tache["état"] == "terminée":
            nb_taches_terminées += 1
    moyenne_temps = temps_total / len(donnees)
    return moyenne_temps, nb_taches_en_cours, nb_taches_terminées

# API pour les données en temps réel
@app.route("/donnees", methods=["GET"])
def donnees_api():
    return jsonify(donnees)

# Route pour afficher le dashboard
@app.route("/")
def index():
    moyenne_temps, nb_taches_en_cours, nb_taches_terminées = calcul_statistiques(donnees)
    return render_template("index.html", donnees=donnees, moyenne_temps=moyenne_temps, nb_taches_en_cours=nb_taches_en_cours, nb_taches_terminées=nb_taches_terminées)

# Route pour créer une nouvelle tâche
@app.route("/creer_tache", methods=["POST"])
def creer_tache():
    nom = request.form["nom"]
    debut = request.form["debut"]
    fin = request.form["fin"]
    etat = "en cours"
    donnees.append({"nom": nom, "début": debut, "fin": fin, "état": etat})
    return jsonify({"message": "Tâche créée avec succès"})

# Route pour mettre à jour un tâche
@app.route("/mettre_a_jour_tache", methods=["POST"])
def mettre_a_jour_tache():
    id_tache = request.form["id"]
    nom = request.form["nom"]
    debut = request.form["debut"]
    fin = request.form["fin"]
    etat = request.form["etat"]
    donnees[int(id_tache)]["nom"] = nom
    donnees[int(id_tache)]["début"] = debut
    donnees[int(id_tache)]["fin"] = fin
    donnees[int(id_tache)]["état"] = etat
    return jsonify({"message": "Tâche mise à jour avec succès"})

# Route pour supprimer un tâche
@app.route("/supprimer_tache", methods=["POST"])
def supprimer_tache():
    id_tache = request.form["id"]
    del donnees[int(id_tache)]
    return jsonify({"message": "Tâche supprimée avec succès"})

# Route pour filtrer les tâches
@app.route("/filtrer_taches", methods=["POST"])
def filtrer_taches():
    etat = request.form["etat"]
    donnees_filtrees = [tache for tache in donnees if tache["état"] == etat]
    return jsonify(donnees_filtrees)

# Route pour trier les tâches
@app.route("/trier_taches", methods=["POST"])
def trier_taches():
    ordre = request.form["ordre"]
    if ordre == "asc":
        donnees_triees = sorted(donnees, key=lambda x: x["nom"])
    elif ordre == "desc":
        donnees_triees = sorted(donnees, key=lambda x: x["nom"], reverse=True)
    return jsonify(donnees_triees)

if __name__ == "__main__":
    app.run(debug=True)
