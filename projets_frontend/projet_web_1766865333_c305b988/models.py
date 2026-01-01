from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from flask_login import LoginManager, UserMixin, login_required, current_user
from datetime import datetime
import time
from random import randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mdp = db.Column(db.String(120), nullable=False)
    historique_connexions = db.Column(db.Text, nullable=False)

class UtilisateurSchema(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Utilisateur):
            return {'id': obj.id, 'email': obj.email, 'mdp': obj.mdp, 'historique_connexions': obj.historique_connexions}
        return super().default(obj)

@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    mdp = generate_password_hash(request.json['mdp'])
    utilisateur = Utilisateur(email=email, mdp=mdp, historique_connexions=json.dumps([]))
    db.session.add(utilisateur)
    db.session.commit()
    return jsonify({'message': 'Utilisateur enregistré'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    mdp = request.json['mdp']
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if utilisateur and check_password_hash(utilisateur.mdp, mdp):
        return jsonify({'message': 'Connexion réussie', 'utilisateur': UtilisateurSchema().encode({'id': utilisateur.id, 'email': utilisateur.email, 'mdp': utilisateur.mdp, 'historique_connexions': utilisateur.historique_connexions})})
    return jsonify({'message': 'Erreur de connexion'})

@app.route('/reinitialisation_mdp', methods=['POST'])
def reinitialisation_mdp():
    email = request.json['email']
    code_sms = randint(100000, 999999)
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if utilisateur:
        # Envoi de code SMS
        msg = MIMEMultipart()
        msg['From'] = 'votre_adresse_email'
        msg['To'] = email
        msg['Subject'] = 'Réinitialisation de mot de passe'
        msg.attach(MIMEText(f'Code de réinitialisation : {code_sms}', 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg['From'], 'votre_mot_de_passe')
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        utilisateur.historique_connexions = json.dumps([{'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'type': 'reinitialisation_mdp', 'code_sms': code_sms}])
        db.session.commit()
        return jsonify({'message': 'Code SMS envoyé'})
    return jsonify({'message': 'Erreur de réinitialisation'})

@app.route('/changer_mdp', methods=['POST'])
def changer_mdp():
    email = request.json['email']
    mdp = request.json['mdp']
    code_sms = request.json['code_sms']
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if utilisateur:
        utilisateur.mdp = generate_password_hash(mdp)
        utilisateur.historique_connexions = json.dumps([{'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'type': 'changement_mdp', 'code_sms': code_sms}])
        db.session.commit()
        return jsonify({'message': 'Mot de passe changé'})
    return jsonify({'message': 'Erreur de changement'})

@app.route('/historique_connexions', methods=['GET'])
@login_required
def historique_connexions():
    utilisateur = Utilisateur.query.get(current_user.id)
    if utilisateur:
        return jsonify({'historique_connexions': utilisateur.historique_connexions})
    return jsonify({'message': 'Erreur d\'accès au historique'})

@app.route('/protection_bruteforce', methods=['POST'])
def protection_bruteforce():
    email = request.json['email']
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    if utilisateur:
        # Vérification du nombre de tentatives
        if len(utilisateur.historique_connexions) > 5:
            return jsonify({'message': 'Trop de tentatives'})
        return jsonify({'message': 'Accès autorisé'})
    return jsonify({'message': 'Erreur de connexion'})

if __name__ == "__main__":
    app.run(debug=True)
