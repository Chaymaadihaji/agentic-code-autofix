import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
Bootstrap(app)

# Chargement des données à partir d'un fichier JSON
def charger_donnees():
    if os.path.exists('donnees.json'):
        with open('donnees.json', 'r') as fichier:
            return json.load(fichier)
    else:
        return []

# Enregistrement des données dans un fichier JSON
def enregistrer_donnees(donnees):
    with open('donnees.json', 'w') as fichier:
        json.dump(donnees, fichier)

# Calcul des statistiques de progression
def calculer_statistiques(donnees):
    total = len(donnees)
    termine = len([tache for tache in donnees if tache['termine']])
    en_cours = len([tache for tache in donnees if not tache['termine']])
    return {
        'total': total,
        'termine': termine,
        'en_cours': en_cours,
        'pourcentage_termine': (termine / total) * 100 if total > 0 else 0
    }

# Création d'une nouvelle tâche
def creer_tache(titre, description):
    donnees = charger_donnees()
    nouvelle_tache = {
        'id': len(donnees) + 1,
        'titre': titre,
        'description': description,
        'termine': False,
        'date_creation': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    donnees.append(nouvelle_tache)
    enregistrer_donnees(donnees)
    return nouvelle_tache

# Édition d'une tâche existante
def editer_tache(id_tache, titre, description):
    donnees = charger_donnees()
    for tache in donnees:
        if tache['id'] == id_tache:
            tache['titre'] = titre
            tache['description'] = description
            enregistrer_donnees(donnees)
            return tache
    return None

# Suppression d'une tâche
def supprimer_tache(id_tache):
    donnees = charger_donnees()
    for tache in donnees:
        if tache['id'] == id_tache:
            donnees.remove(tache)
            enregistrer_donnees(donnees)
            return True
    return False

# Marquer une tâche comme terminée
def marquer_tache_terminee(id_tache):
    donnees = charger_donnees()
    for tache in donnees:
        if tache['id'] == id_tache:
            tache['termine'] = True
            enregistrer_donnees(donnees)
            return True
    return False

# Route pour la page d'accueil
@app.route('/')
def accueil():
    donnees = charger_donnees()
    statistiques = calculer_statistiques(donnees)
    return render_template('accueil.html', donnees=donnees, statistiques=statistiques)

# Route pour la création d'une nouvelle tâche
@app.route('/creer', methods=['POST'])
def creer():
    titre = request.form['titre']
    description = request.form['description']
    nouvelle_tache = creer_tache(titre, description)
    return jsonify({'message': 'Tâche créée avec succès', 'tache': nouvelle_tache})

# Route pour l'édition d'une tâche existante
@app.route('/editer/<int:id_tache>', methods=['POST'])
def editer(id_tache):
    titre = request.form['titre']
    description = request.form['description']
    tache_editee = editer_tache(id_tache, titre, description)
    if tache_editee:
        return jsonify({'message': 'Tâche éditée avec succès', 'tache': tache_editee})
    else:
        return jsonify({'message': 'Tâche non trouvée'}), 404

# Route pour la suppression d'une tâche
@app.route('/supprimer/<int:id_tache>', methods=['POST'])
def supprimer(id_tache):
    if supprimer_tache(id_tache):
        return jsonify({'message': 'Tâche supprimée avec succès'})
    else:
        return jsonify({'message': 'Tâche non trouvée'}), 404

# Route pour marquer une tâche comme terminée
@app.route('/terminer/<int:id_tache>', methods=['POST'])
def terminer(id_tache):
    if marquer_tache_terminee(id_tache):
        return jsonify({'message': 'Tâche marquée comme terminée avec succès'})
    else:
        return jsonify({'message': 'Tâche non trouvée'}), 404

if __name__ == "__main__":
    app.run(debug=True)
