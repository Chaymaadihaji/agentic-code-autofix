python
# Importations
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from sqlalchemy import func
from datetime import datetime, timedelta
import os
import csv
from fpdf import FPDF
import sqlite3
from config import Config
from models import db, ma, User, Book, Loan, Stat
from api import api
from dashboard import dashboard
from utils import send_email, get_stats

# Application
app = Flask(__name__)
app.config.from_object(Config)

# Gestion de la base de données
db.init_app(app)

# Authentification
ma.init_app(app)
mail = Mail(app)
jwt = JWTManager(app)

# API
api.init_app(app)

# Dashboard
dashboard.init_app(app)

# Routes
@app.route('/')
def index():
    return 'Bienvenue dans la bibliothèque en ligne !'

@app.route('/inscription', methods=['POST'])
def inscription():
    try:
        user = User(
            username=request.json['username'],
            email=request.json['email'],
            password=request.json['password']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Inscription réussie !'}), 201
    except Exception as e:
        return jsonify({'message': 'Erreur d\'inscription : ' + str(e)}), 400

@app.route('/connexion', methods=['POST'])
def connexion():
    try:
        user = User.query.filter_by(username=request.json['username']).first()
        if user and user.password == request.json['password']:
            access_token = create_access_token(identity=user.id)
            return jsonify({'token': access_token}), 200
        else:
            return jsonify({'message': 'Identifiants incorrects'}), 401
    except Exception as e:
        return jsonify({'message': 'Erreur de connexion : ' + str(e)}), 400

@app.route('/deconnexion')
@jwt_required
def deconnexion():
    return jsonify({'message': 'Déconnexion réussie !'}), 200

@app.route('/livres', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required
def livres():
    if request.method == 'GET':
        livres = Book.query.all()
        return jsonify([book.to_dict() for book in livres]), 200
    elif request.method == 'POST':
        try:
            book = Book(
                title=request.json['title'],
                author=request.json['author'],
                publication_date=request.json['publication_date']
            )
            db.session.add(book)
            db.session.commit()
            return jsonify({'message': 'Livre ajouté avec succès !'}), 201
        except Exception as e:
            return jsonify({'message': 'Erreur d\'ajout : ' + str(e)}), 400
    elif request.method == 'PUT':
        try:
            book = Book.query.get(request.json['id'])
            if book:
                book.title = request.json['title']
                book.author = request.json['author']
                book.publication_date = request.json['publication_date']
                db.session.commit()
                return jsonify({'message': 'Livre modifié avec succès !'}), 200
            else:
                return jsonify({'message': 'Livre non trouvé'}), 404
        except Exception as e:
            return jsonify({'message': 'Erreur de modification : ' + str(e)}), 400
    elif request.method == 'DELETE':
        try:
            book = Book.query.get(request.json['id'])
            if book:
                db.session.delete(book)
                db.session.commit()
                return jsonify({'message': 'Livre supprimé avec succès !'}), 200
            else:
                return jsonify({'message': 'Livre non trouvé'}), 404
        except Exception as e:
            return jsonify({'message': 'Erreur de suppression : ' + str(e)}), 400

@app.route('/emprunts', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required
def emprunts():
    if request.method == 'GET':
        emprunts = Loan.query.all()
        return jsonify([emprunt.to_dict() for emprunt in emprunts]), 200
    elif request.method == 'POST':
        try:
            emprunt = Loan(
                user_id=request.json['user_id'],
                book_id=request.json['book_id'],
                start_date=request.json['start_date'],
                end_date=request.json['end_date']
            )
            db.session.add(emprunt)
            db.session.commit()
            return jsonify({'message': 'Emprunt ajouté avec succès !'}), 201
        except Exception as e:
            return jsonify({'message': 'Erreur d\'ajout : ' + str(e)}), 400
    elif request.method == 'PUT':
        try:
            emprunt = Loan.query.get(request.json['id'])
            if emprunt:
                emprunt.start_date = request.json['start_date']
                emprunt.end_date = request.json['end_date']
                db.session.commit()
                return jsonify({'message': 'Emprunt modifié avec succès !'}), 200
            else:
                return jsonify({'message': 'Emprunt non trouvé'}), 404
        except Exception as e:
            return jsonify({'message': 'Erreur de modification : ' + str(e)}), 400
    elif request.method == 'DELETE':
        try:
            emprunt = Loan.query.get(request.json['id'])
            if emprunt:
                db.session.delete(emprunt)
                db.session.commit()
                return jsonify({'message': 'Emprunt supprimé avec succès !'}), 200
            else:
                return jsonify({'message': 'Emprunt non trouvé'}), 404
        except Exception as e:
            return jsonify({'message': 'Erreur de suppression : ' + str(e)}), 400

@app.route('/recherche', methods=['GET'])
def recherche():
    try:
        q = request.args.get('q')
        livres = Book.query.filter(Book.title.like('%' + q + '%')).all()
        return jsonify([book.to_dict() for book in livres]), 200
    except Exception as e:
        return jsonify({'message': 'Erreur de recherche : ' + str(e)}), 400

@app.route('/recommandations')
@jwt_required
def recommandations():
    try:
        historique = Loan.query.filter(Loan.user_id == request.json['user_id']).all()
        recommandations = []
        for emprunt in historique:
            book = Book.query.get(emprunt.book_id)
            recommandations.append(book.title)
        return jsonify({'recommandations': recommandations}), 200
    except Exception as e:
        return jsonify({'message': 'Erreur de recommandations : ' + str(e)}), 400

@app.route('/export/csv')
def export_csv():
    try:
        livres = Book.query.all()
        with open('livres.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Titre', 'Auteur', 'Date de publication'])
            for livre in livres:
                writer.writerow([livre.title, livre.author, livre.publication_date])
        return jsonify({'message': 'Export CSV réussi !'}), 200
    except Exception as e:
        return jsonify({'message': 'Erreur d\'export CSV : ' + str(e)}), 400

@app.route('/export/pdf')
def export_pdf():
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Livres', 0, 1, 'C')
        pdf.ln(10)
        livres = Book.query.all()
        for livre in livres:
            pdf.cell(0, 10, str(livre.title), 0, 1, 'L')
            pdf.cell(0, 10, str(livre.author), 0, 1, 'L')
            pdf.cell(0, 10, str(livre.publication_date), 0, 1, 'L')
            pdf.ln(10)
        pdf.output('livres.pdf')
        return jsonify({'message': 'Export PDF réussi !'}), 200
    except Exception as e:
        return jsonify({'message': 'Erreur d\'export PDF : ' + str(e)}), 400

# Gestion des erreurs
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Ressource non trouvée'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Erreur interne du serveur'}), 500

# Début de l'application
if __name__ == '__main__':
    app.run(debug=True)
