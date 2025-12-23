import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap
import matplotlib.pyplot as plt

app = Flask(__name__)
Bootstrap(app)

# Chargement des données à partir d'un fichier JSON
def charger_donnees():
    if os.path.exists('donnees.json'):
        with open('donnees.json', 'r') as fichier:
            return json.load(fichier)
    else:
        return {'taches': []}

# Sauvegarde des données dans un fichier JSON
def sauvegarder_donnees(donnees):
    with open('donnees.json', 'w') as fichier:
        json.dump(donnees, fichier)

# Calcul des statistiques
def calculer_statistiques(donnees):
    total_taches = len(donnees['taches'])
    taches_terminees = sum(1 for tache in donnees['taches'] if tache['terminee'])
    progression = (taches_terminees / total_taches) * 100 if total_taches > 0 else 0
    return {
        'total_taches': total_taches,
        'taches_terminees': taches_terminees,
        'progression': progression
    }

# Génération du graphique de progression
def generer_graphique(donnees):
    statistiques = calculer_statistiques(donnees)
    plt.bar(['Tâches terminées', 'Tâches en cours'], [statistiques['taches_terminees'], statistiques['total_taches'] - statistiques['taches_terminees']])
    plt.xlabel('État des tâches')
    plt.ylabel('Nombre de tâches')
    plt.title('Progression des tâches')
    plt.savefig('static/graphique.png')

# Route pour la page d'accueil
@app.route('/')
def accueil():
    donnees = charger_donnees()
    statistiques = calculer_statistiques(donnees)
    generer_graphique(donnees)
    return render_template('accueil.html', donnees=donnees, statistiques=statistiques)

# Route pour la création d'une tâche
@app.route('/creer_tache', methods=['POST'])
def creer_tache():
    donnees = charger_donnees()
    tache = {
        'id': len(donnees['taches']) + 1,
        'nom': request.form['nom'],
        'description': request.form['description'],
        'terminee': False
    }
    donnees['taches'].append(tache)
    sauvegarder_donnees(donnees)
    return jsonify({'message': 'Tâche créée avec succès'})

# Route pour l'édition d'une tâche
@app.route('/editer_tache/<int:id>', methods=['POST'])
def editer_tache(id):
    donnees = charger_donnees()
    for tache in donnees['taches']:
        if tache['id'] == id:
            tache['nom'] = request.form['nom']
            tache['description'] = request.form['description']
            sauvegarder_donnees(donnees)
            return jsonify({'message': 'Tâche éditée avec succès'})
    return jsonify({'message': 'Tâche non trouvée'})

# Route pour la suppression d'une tâche
@app.route('/supprimer_tache/<int:id>')
def supprimer_tache(id):
    donnees = charger_donnees()
    for tache in donnees['taches']:
        if tache['id'] == id:
            donnees['taches'].remove(tache)
            sauvegarder_donnees(donnees)
            return jsonify({'message': 'Tâche supprimée avec succès'})
    return jsonify({'message': 'Tâche non trouvée'})

# Route pour la mise à jour de l'état d'une tâche
@app.route('/mettre_a_jour_etat/<int:id>')
def mettre_a_jour_etat(id):
    donnees = charger_donnees()
    for tache in donnees['taches']:
        if tache['id'] == id:
            tache['terminee'] = not tache['terminee']
            sauvegarder_donnees(donnees)
            return jsonify({'message': 'État de la tâche mis à jour avec succès'})
    return jsonify({'message': 'Tâche non trouvée'})

if __name__ == "__main__":
    app.run(debug=True)
