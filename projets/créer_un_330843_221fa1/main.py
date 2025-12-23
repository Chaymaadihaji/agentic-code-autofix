# main.py

import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Chemin pour les fichiers de données
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')

# Initialisation des données
data = [
    {'id': 1, 'nom': 'Tâche 1', 'état': 'En cours', 'durée': 10},
    {'id': 2, 'nom': 'Tâche 2', 'état': 'Terminé', 'durée': 20},
    {'id': 3, 'nom': 'Tâche 3', 'état': 'En cours', 'durée': 30},
]

# Initialisation des statistiques
stats = {
    'total': len(data),
    'en_cours': sum(1 for t in data if t['état'] == 'En cours'),
    'terminé': sum(1 for t in data if t['état'] == 'Terminé'),
}

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html', data=data, stats=stats)

# Route pour récupérer les données en temps réel
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

# Route pour ajouter une nouvelle tâche
@app.route('/ajouter', methods=['POST'])
def ajouter_tache():
    nouveau = {
        'id': len(data) + 1,
        'nom': request.form['nom'],
        'état': 'En cours',
        'durée': int(request.form['durée']),
    }
    data.append(nouveau)
    stats['total'] += 1
    stats['en_cours'] += 1
    return jsonify({'message': 'Tâche ajoutée avec succès'})

# Route pour supprimer une tâche
@app.route('/supprimer/<int:id>', methods=['GET'])
def supprimer_tache(id):
    for i, t in enumerate(data):
        if t['id'] == id:
            del data[i]
            stats['total'] -= 1
            if t['état'] == 'En cours':
                stats['en_cours'] -= 1
            else:
                stats['terminé'] -= 1
            return jsonify({'message': 'Tâche supprimée avec succès'})
    return jsonify({'message': 'Tâche non trouvée'}), 404

# Route pour mettre à jour l'état d'une tâche
@app.route('/miser_a_jour/<int:id>', methods=['POST'])
def mettre_a_jour_tache(id):
    for t in data:
        if t['id'] == id:
            t['état'] = request.form['état']
            if t['état'] == 'Terminé':
                stats['terminé'] += 1
                stats['en_cours'] -= 1
            return jsonify({'message': 'État mis à jour avec succès'})
    return jsonify({'message': 'Tâche non trouvée'}), 404

# Route pour afficher les statistiques
@app.route('/stats', methods=['GET'])
def afficher_stats():
    return jsonify(stats)

# Route pour afficher un graphique
@app.route('/graphique', methods=['GET'])
def afficher_graphique():
    df = pd.DataFrame(data)
    sns.set()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='état', y='durée', data=df)
    plt.title('Durée par état')
    plt.xlabel('État')
    plt.ylabel('Durée')
    plt.show()
    return 'Graphique affiché'

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
