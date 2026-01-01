from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'votre_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'votre_mot_de_passe'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mail = Mail(app)

s = URLSafeTimedSerializer('secret_key_here')

class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(120), nullable=False)

class Connexion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        utilisateur = Utilisateur.query.filter_by(email=request.form['email']).first()
        if utilisateur and bcrypt.check_password_hash(utilisateur.mot_de_passe, request.form['mot_de_passe']):
            login_user(utilisateur)
            return redirect(url_for('accueil'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        utilisateur = Utilisateur(nom=request.form['nom'], prenom=request.form['prenom'], email=request.form['email'], mot_de_passe=bcrypt.generate_password_hash(request.form['mot_de_passe']).decode('utf-8'))
        db.session.add(utilisateur)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/accueil')
@login_required
def accueil():
    return render_template('accueil.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/historique')
@login_required
def historique():
    connexions = Connexion.query.all()
    return render_template('historique.html', connexions=connexions)

@app.route('/connexion', methods=['POST'])
@login_required
def connexion():
    connexion = Connexion(utilisateur_id=current_user.id)
    db.session.add(connexion)
    db.session.commit()
    return 'Connexion enregistrée'

@app.route('/validation_email', methods=['POST'])
@login_required
def validation_email():
    email = current_user.email
    msg = MIMEMultipart()
    msg['From'] = 'votre_email@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'Validation de compte'
    body = 'Cliquez sur le lien suivant pour valider votre compte : http://localhost:5000/validation/' + s.dumps(email)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], 'votre_mot_de_passe')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()
    return 'Email envoyé'

@app.route('/validation/<token>')
def validation(token):
    email = s.loads(token)
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    utilisateur.valide = True
    db.session.commit()
    return 'Compte validé'

@app.route('/reinitialisation_mot_de_passe', methods=['POST'])
@login_required
def reinitialisation_mot_de_passe():
    email = current_user.email
    msg = MIMEMultipart()
    msg['From'] = 'votre_email@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'Réinitialisation de mot de passe'
    body = 'Cliquez sur le lien suivant pour réinitialiser votre mot de passe : http://localhost:5000/reinitialisation/' + s.dumps(email)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], 'votre_mot_de_passe')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()
    return 'Email envoyé'

@app.route('/reinitialisation/<token>')
def reinitialisation(token):
    email = s.loads(token)
    utilisateur = Utilisateur.query.filter_by(email=email).first()
    utilisateur.mot_de_passe = bcrypt.generate_password_hash(request.form['mot_de_passe']).decode('utf-8')
    db.session.commit()
    return 'Mot de passe réinitialisé'

@app.route('/protection_contre_attaques_bruteforce', methods=['POST'])
@login_required
def protection_contre_attaques_bruteforce():
    utilisateur = Utilisateur.query.filter_by(email=current_user.email).first()
    if utilisateur.mauvais_mot_de_passe >= 5:
        utilisateur.bloque = True
        db.session.commit()
        return 'Compte bloqué'
    return 'Mauvais mot de passe'

@app.route('/historique_connexions')
@login_required
def historique_connexions():
    connexions = Connexion.query.all()
    return render_template('historique_connexions.html', connexions=connexions)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
