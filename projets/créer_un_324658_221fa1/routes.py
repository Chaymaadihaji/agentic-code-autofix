# Importation des bibliothèques nécessaires
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import json
import random

# Création de l'application Flask
app = Flask(__name__)
Bootstrap(app)

# Données de tâches en mémoire (pour simplifier, on utilise un dictionnaire)
taches = {
    1: {"titre": "Tâche 1", "description": "Description de la tâche 1", "etat": "en_cours"},
    2: {"titre": "Tâche 2", "description": "Description de la tâche 2", "etat": "termine"},
    3: {"titre": "Tâche 3", "description": "Description de la tâche 3", "etat": "en_cours"}
}

# Route pour la page d'accueil
@app.route("/")
def accueil():
    # Récupération des tâches
    taches_list = list(taches.values())
    
    # Calcul des statistiques
    en_cours = len([tache for tache in taches_list if tache["etat"] == "en_cours"])
    termine = len([tache for tache in taches_list if tache["etat"] == "termine"])
    
    # Affichage de la page d'accueil
    return render_template("accueil.html", taches=taches_list, en_cours=en_cours, termine=termine)

# Route pour la création d'une tâche
@app.route("/creer_tache", methods=["POST"])
def creer_tache():
    # Récupération des données de la tâche
    titre = request.form["titre"]
    description = request.form["description"]
    etat = "en_cours"
    
    # Ajout de la tâche à la liste
    id_tache = max(taches.keys()) + 1
    taches[id_tache] = {"titre": titre, "description": description, "etat": etat}
    
    # Retour à la page d'accueil
    return jsonify({"message": "Tâche créée avec succès"})

# Route pour l'édition d'une tâche
@app.route("/editer_tache/<int:id_tache>", methods=["POST"])
def editer_tache(id_tache):
    # Récupération des données de la tâche
    titre = request.form["titre"]
    description = request.form["description"]
    etat = request.form["etat"]
    
    # Mise à jour de la tâche
    taches[id_tache] = {"titre": titre, "description": description, "etat": etat}
    
    # Retour à la page d'accueil
    return jsonify({"message": "Tâche mise à jour avec succès"})

# Route pour la suppression d'une tâche
@app.route("/supprimer_tache/<int:id_tache>")
def supprimer_tache(id_tache):
    # Suppression de la tâche
    del taches[id_tache]
    
    # Retour à la page d'accueil
    return jsonify({"message": "Tâche supprimée avec succès"})

# Route pour les données en temps réel
@app.route("/donnees_temps_reel")
def donnees_temps_reel():
    # Récupération des tâches
    taches_list = list(taches.values())
    
    # Calcul des statistiques
    en_cours = len([tache for tache in taches_list if tache["etat"] == "en_cours"])
    termine = len([tache for tache in taches_list if tache["etat"] == "termine"])
    
    # Retour des données en JSON
    return jsonify({"en_cours": en_cours, "termine": termine})

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
