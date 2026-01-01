python
# models.py

from flask import current_app
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from email.message import EmailMessage
import smtplib
import csv
import io
from fpdf import FPDF

db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='utilisateur')

    def set_password(self, mot_de_passe):
        self.mot_de_passe = generate_password_hash(mot_de_passe)

    def check_password(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe, mot_de_passe)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    editeur = db.Column(db.String(100), nullable=False)
    date_publication = db.Column(db.Date, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date_emprunt = db.Column(db.Date, nullable=False)
    date_retour = db.Column(db.Date, nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def send_email(email, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Notification'
    msg['From'] = 'your-email@example.com'
    msg['To'] = email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your-email@example.com', 'your-password')
        smtp.send_message(msg)

def export_csv():
    with current_app.open_resource('static/csv/livres.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Titre', 'Auteur', 'Editeur', 'Date de publication', 'Quantité'])
        for livre in Livre.query.all():
            writer.writerow([livre.titre, livre.auteur, livre.editeur, livre.date_publication, livre.quantite])

def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(0, 10, 'Liste des livres', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    for livre in Livre.query.all():
        pdf.cell(0, 10, f"{livre.titre} - {livre.auteur}", 0, 1, 'L')
        pdf.ln(5)
    pdf.output('static/pdf/livres.pdf', 'F')
