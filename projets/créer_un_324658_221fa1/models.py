# Importation des bibliothèques nécessaires
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

# Création de l'application Flask
app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taches.db'
db = SQLAlchemy(app)

# Modèle de données pour les tâches
class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    etat = db.Column(db.String(50), nullable=False, default='En cours')
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Tache({self.titre}, {self.description}, {self.etat})'

# Création de la base de données
with app.app_context():
    db.create_all()

# Route pour la page d'accueil
@app.route('/')
def index():
    taches = Tache.query.all()
    return render_template('index.html', taches=taches)

# Route pour créer une nouvelle tâche
@app.route('/creer_tache', methods=['POST'])
def creer_tache():
    titre = request.form['titre']
    description = request.form['description']
    tache = Tache(titre=titre, description=description)
    db.session.add(tache)
    db.session.commit()
    return jsonify({'message': 'Tâche créée avec succès'}), 201

# Route pour éditer une tâche
@app.route('/editer_tache/<int:id>', methods=['PUT'])
def editer_tache(id):
    tache = Tache.query.get_or_404(id)
    tache.titre = request.form['titre']
    tache.description = request.form['description']
    db.session.commit()
    return jsonify({'message': 'Tâche éditée avec succès'}), 200

# Route pour supprimer une tâche
@app.route('/supprimer_tache/<int:id>', methods=['DELETE'])
def supprimer_tache(id):
    tache = Tache.query.get_or_404(id)
    db.session.delete(tache)
    db.session.commit()
    return jsonify({'message': 'Tâche supprimée avec succès'}), 200

# Route pour afficher les statistiques de progression
@app.route('/statistiques')
def statistiques():
    taches = Tache.query.all()
    taches_en_cours = [tache for tache in taches if tache.etat == 'En cours']
    taches_terminees = [tache for tache in taches if tache.etat == 'Terminée']
    return render_template('statistiques.html', taches_en_cours=len(taches_en_cours), taches_terminees=len(taches_terminees))

# Lancement de l'application
if __name__ == '__main__':
    app.run(debug=True)
