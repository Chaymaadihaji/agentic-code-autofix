# dashboard.py

import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_bootstrap4 import Bootstrap
from datetime import datetime, timedelta

app = Flask(__name__)
Bootstrap(app)

# Connexion à la base de données
conn = sqlite3.connect('taches.db')
cursor = conn.cursor()

# Créer la table des tâches s'il n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS taches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        description TEXT,
        cree_le DATE DEFAULT CURRENT_DATE,
        termine_le DATE
    )
''')

# Génération de données pour le dashboard
taches = [
    {'nom': 'Tâche 1', 'description': 'Description de la tâche 1'},
    {'nom': 'Tâche 2', 'description': 'Description de la tâche 2'},
    {'nom': 'Tâche 3', 'description': 'Description de la tâche 3'}
]

# Calcul des statistiques/métriques
statistiques = {
    'total_taches': len(taches),
    'taches_terminees': 0,
    'taches_en_cours': 0,
    'taches_a_comecer': 0
}

for tache in taches:
    if tache['termine_le']:
        statistiques['taches_terminees'] += 1
    elif tache['cree_le'] + timedelta(days=7) > datetime.now():
        statistiques['taches_en_cours'] += 1
    else:
        statistiques['taches_a_comecer'] += 1

# API pour les données en temps réel
@app.route('/taches', methods=['GET'])
def get_taches():
    return jsonify(taches)

# Ajout et suppression de tâches
@app.route('/taches', methods=['POST'])
def ajout_tache():
    nom = request.json['nom']
    description = request.json.get('description', '')
    cree_le = datetime.now()
    termine_le = None
    if 'termine_le' in request.json:
        termine_le = request.json['termine_le']
    cursor.execute("INSERT INTO taches (nom, description, cree_le, termine_le) VALUES (?, ?, ?, ?)",
                   (nom, description, cree_le, termine_le))
    conn.commit()
    return jsonify({'success': True})

@app.route('/taches/<int:id>', methods=['DELETE'])
def supprimer_tache(id):
    cursor.execute("DELETE FROM taches WHERE id = ?", (id,))
    conn.commit()
    return jsonify({'success': True})

# Filtrage et tri des tâches
@app.route('/taches', methods=['GET'])
def filtrer_taches():
    filter_ = request.args.get('filter')
    tri = request.args.get('tri')
    if filter_:
        taches_filtrees = [tache for tache in taches if filter_ in tache['nom'] or filter_ in tache['description']]
    else:
        taches_filtrees = taches
    if tri:
        taches_triees = sorted(taches_filtrees, key=lambda tache: tache[tri])
    else:
        taches_triees = taches_filtrees
    return jsonify(taches_triees)

# Vue de base pour le dashboard
@app.route('/')
def index():
    return render_template('index.html', taches=taches, statistiques=statistiques)

if __name__ == "__main__":
    app.run(debug=True)
