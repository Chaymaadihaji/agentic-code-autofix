# utils.py

import sqlite3
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource
from streamlit import run
from PIL import Image
from fpdf import FPDF
import json
from datetime import datetime

# Configuration
config = {
    'SECRET_KEY': 'secret',
    'DB_NAME': 'library.db'
}

# Création de la base de données
conn = sqlite3.connect(config['DB_NAME'])
cursor = conn.cursor()

# Création des tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY,
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL,
        isbn TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS membres (
        id INTEGER PRIMARY KEY,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT NOT NULL,
        mot_de_passe TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS emprunts (
        id INTEGER PRIMARY KEY,
        livre_id INTEGER NOT NULL,
        membre_id INTEGER NOT NULL,
        date_emprunt DATE NOT NULL,
        date_rendu DATE,
        FOREIGN KEY (livre_id) REFERENCES livres (id),
        FOREIGN KEY (membre_id) REFERENCES membres (id)
    );
''')

# Création de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config['SECRET_KEY']
jwt = JWTManager(app)

# API REST pour mobile
api = Api(app)

# Route pour les livres
class Livre(Resource):
    def get(self, id):
        cursor.execute('SELECT * FROM livres WHERE id = ?', (id,))
        livre = cursor.fetchone()
        return jsonify({'id': livre[0], 'titre': livre[1], 'auteur': livre[2], 'isbn': livre[3]})

    def post(self):
        data = request.get_json()
        cursor.execute('INSERT INTO livres (titre, auteur, isbn) VALUES (?, ?, ?)', (data['titre'], data['auteur'], data['isbn']))
        conn.commit()
        return jsonify({'message': 'Livre ajouté avec succès'})

class Livres(Resource):
    def get(self):
        cursor.execute('SELECT * FROM livres')
        livres = cursor.fetchall()
        return jsonify([{'id': livre[0], 'titre': livre[1], 'auteur': livre[2], 'isbn': livre[3]} for livre in livres])

# Route pour les membres
class Membre(Resource):
    def get(self, id):
        cursor.execute('SELECT * FROM membres WHERE id = ?', (id,))
        membre = cursor.fetchone()
        return jsonify({'id': membre[0], 'nom': membre[1], 'prenom': membre[2], 'email': membre[3], 'mot_de_passe': membre[4]})

    def post(self):
        data = request.get_json()
        cursor.execute('INSERT INTO membres (nom, prenom, email, mot_de_passe) VALUES (?, ?, ?, ?)', (data['nom'], data['prenom'], data['email'], data['mot_de_passe']))
        conn.commit()
        return jsonify({'message': 'Membre ajouté avec succès'})

class Membres(Resource):
    def get(self):
        cursor.execute('SELECT * FROM membres')
        membres = cursor.fetchall()
        return jsonify([{'id': membre[0], 'nom': membre[1], 'prenom': membre[2], 'email': membre[3], 'mot_de_passe': membre[4]} for membre in membres])

# Route pour les emprunts
class Emprunt(Resource):
    def get(self, id):
        cursor.execute('SELECT * FROM emprunts WHERE id = ?', (id,))
        emprunt = cursor.fetchone()
        return jsonify({'id': emprunt[0], 'livre_id': emprunt[1], 'membre_id': emprunt[2], 'date_emprunt': emprunt[3], 'date_rendu': emprunt[4]})

    def post(self):
        data = request.get_json()
        cursor.execute('INSERT INTO emprunts (livre_id, membre_id, date_emprunt) VALUES (?, ?, ?)', (data['livre_id'], data['membre_id'], data['date_emprunt']))
        conn.commit()
        return jsonify({'message': 'Emprunt effectué avec succès'})

class Emprunts(Resource):
    def get(self):
        cursor.execute('SELECT * FROM emprunts')
        emprunts = cursor.fetchall()
        return jsonify([{'id': emprunt[0], 'livre_id': emprunt[1], 'membre_id': emprunt[2], 'date_emprunt': emprunt[3], 'date_rendu': emprunt[4]} for emprunt in emprunts])

# Route pour l'authentification
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cursor.execute('SELECT * FROM membres WHERE email = ? AND mot_de_passe = ?', (data['email'], data['mot_de_passe']))
    membre = cursor.fetchone()
    if membre:
        access_token = create_access_token(identity=membre[0])
        return jsonify({'access_token': access_token})
    return jsonify({'message': 'Identifiants incorrects'}), 401

# Route pour la génération de rapports PDF
@app.route('/rapport', methods=['GET'])
@jwt_required
def rapport():
    membre_id = get_jwt_identity()
    cursor.execute('SELECT * FROM emprunts WHERE membre_id = ?', (membre_id,))
    emprunts = cursor.fetchall()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Rapport d'emprunts", ln = True, align = 'C')
    pdf.ln(10)
    for emprunt in emprunts:
        pdf.cell(200, 10, txt = f"Livre {emprunt[1]} emprunté le {emprunt[3]}", ln = True, align = 'L')
    pdf.output("rapport.pdf")
    return jsonify({'message': 'Rapport généré avec succès'})

# Route pour le dashboard
@app.route('/dashboard', methods=['GET'])
@jwt_required
def dashboard():
    membre_id = get_jwt_identity()
    cursor.execute('SELECT * FROM emprunts WHERE membre_id = ?', (membre_id,))
    emprunts = cursor.fetchall()
    return jsonify({'emprunts': [f"Livre {emprunt[1]} emprunté le {emprunt[3]}" for emprunt in emprunts]})

# Route pour les formulaires
@app.route('/formulaires', methods=['GET', 'POST'])
def formulaires():
    if request.method == 'POST':
        data = request.get_json()
        if data['type'] == 'livre':
            cursor.execute('INSERT INTO livres (titre, auteur, isbn) VALUES (?, ?, ?)', (data['titre'], data['auteur'], data['isbn']))
            conn.commit()
            return jsonify({'message': 'Livre ajouté avec succès'})
        elif data['type'] == 'membre':
            cursor.execute('INSERT INTO membres (nom, prenom, email, mot_de_passe) VALUES (?, ?, ?, ?)', (data['nom'], data['prenom'], data['email'], data['mot_de_passe']))
            conn.commit()
            return jsonify({'message': 'Membre ajouté avec succès'})
        elif data['type'] == 'emprunt':
            cursor.execute('INSERT INTO emprunts (livre_id, membre_id, date_emprunt) VALUES (?, ?, ?)', (data['livre_id'], data['membre_id'], data['date_emprunt']))
            conn.commit()
            return jsonify({'message': 'Emprunt effectué avec succès'})
    return jsonify({'message': 'Formulaire envoyé avec succès'})

# Route pour les tableaux
@app.route('/tableaux', methods=['GET'])
def tableaux():
    cursor.execute('SELECT * FROM livres')
    livres = cursor.fetchall()
    return jsonify({'livres': [{'id': livre[0], 'titre': livre[1], 'auteur': livre[2], 'isbn': livre[3]} for livre in livres]})

# Route pour les graphiques
@app.route('/graphiques', methods=['GET'])
def graphiques():
    cursor.execute('SELECT * FROM emprunts')
    emprunts = cursor.fetchall()
    return jsonify({'emprunts': [{'id': emprunt[0], 'livre_id': emprunt[1], 'membre_id': emprunt[2], 'date_emprunt': emprunt[3], 'date_rendu': emprunt[4]} for emprunt in emprunts]})

# Route pour les filtres
@app.route('/filtres', methods=['GET', 'POST'])
def filtres():
    if request.method == 'POST':
        data = request.get_json()
        cursor.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + data['titre'] + '%',))
        livres = cursor.fetchall()
        return jsonify({'livres': [{'id': livre[0], 'titre': livre[1], 'auteur': livre[2], 'isbn': livre[3]} for livre in livres]})
    return jsonify({'message': 'Filtre appliqué avec succès'})

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True)
