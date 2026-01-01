from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_bootstrap import Bootstrap
from flask_sslify import SSLify
import os
from datetime import datetime
from flask import send_file
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projets_frontend\projet_web_1766865214_c305b988\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page'
login_manager.login_message_category = 'info'
Bootstrap(app)
sslify = SSLify(app)

class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    motdepasse = db.Column(db.String(128))
    historique = db.relationship('Historique', backref='utilisateur', lazy=True)

class Historique(db.Model):
    __tablename__ = 'historique'
    id = db.Column(db.Integer, primary_key=True)
    utilisateurs_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login_manager.user_loader
def load_user(id):
    return Utilisateur.query.get(int(id))

class ConnexionForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    motdepasse = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class InscriptionForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    motdepasse = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_motdepasse = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('motdepasse')])
    submit = SubmitField('S\'inscrire')

class MotdepasseOublieForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Récupérer le mot de passe')

class EnvoiSMSForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Envoyer le SMS')

class HistoriqueForm(FlaskForm):
    submit = SubmitField('Afficher l\'historique')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ConnexionForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(pseudo=form.pseudo.data).first()
        if utilisateur and check_password_hash(utilisateur.motdepasse, form.motdepasse.data):
            login_user(utilisateur)
            return redirect(url_for('historique'))
    return render_template('index.html', title='Connexion', form=form)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur(pseudo=form.pseudo.data, email=form.email.data, motdepasse=generate_password_hash(form.motdepasse.data))
        db.session.add(utilisateur)
        db.session.commit()
        return redirect(url_for('connexion'))
    return render_template('inscription.html', title='Inscription', form=form)

@app.route('/connexion', methods=['GET', 'POST'])
@login_required
def connexion():
    form = EnvoiSMSForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(email=form.email.data).first()
        if utilisateur:
            # Envoi du SMS
            msg = MIMEMultipart()
            msg['From'] = 'votre_adresse_email@gmail.com'
            msg['To'] = form.email.data
            msg['Subject'] = 'Réinitialisation du mot de passe'
            body = 'Votre lien de réinitialisation est: http://localhost:5000/reinitialisation'
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(msg['From'], 'votre_mot_de_passe')
            text = msg.as_string()
            server.sendmail(msg['From'], msg['To'], text)
            server.quit()
            return redirect(url_for('reinitialisation'))
    return render_template('connexion.html', title='Connexion', form=form)

@app.route('/reinitialisation', methods=['GET', 'POST'])
def reinitialisation():
    form = MotdepasseOublieForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(email=form.email.data).first()
        if utilisateur:
            # Envoi du SMS
            msg = MIMEMultipart()
            msg['From'] = 'votre_adresse_email@gmail.com'
            msg['To'] = form.email.data
            msg['Subject'] = 'Réinitialisation du mot de passe'
            body = 'Votre lien de réinitialisation est: http://localhost:5000/reinitialisation'
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(msg['From'], 'votre_mot_de_passe')
            text = msg.as_string()
            server.sendmail(msg['From'], msg['To'], text)
            server.quit()
            return redirect(url_for('reinitialisation'))
    return render_template('reinitialisation.html', title='Réinitialisation', form=form)

@app.route('/historique', methods=['GET', 'POST'])
@login_required
def historique():
    form = HistoriqueForm()
    if form.validate_on_submit():
        return redirect(url_for('historique'))
    return render_template('historique.html', title='Historique', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/historique', methods=['GET'])
@login_required
def api_historique():
    historiques = Historique.query.all()
    return jsonify([{'date': h.date, 'utilisateur_id': h.utilisateurs.id} for h in historiques])

if __name__ == "__main__":
    app.run(debug=True)
