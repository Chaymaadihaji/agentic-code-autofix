# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import flask_smg
import smtplib
from email.message import EmailMessage
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)

# Modèle de l'utilisateur
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(120), nullable=False)

# Modèle de la connexion
class Connexion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur and bcrypt.check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
            return redirect(url_for('accueil'))
    return render_template('login.html')

# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur(email=email, mot_de_passe=bcrypt.generate_password_hash(mot_de_passe).decode('utf-8'))
        db.session.add(utilisateur)
        db.session.commit()
        return redirect(url_for('accueil'))
    return render_template('register.html')

# Route de réinitialisation du mot de passe
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur:
            utilisateur.mot_de_passe = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
            db.session.commit()
            return redirect(url_for('accueil'))
    return render_template('reset_password.html')

# Route de l'historique des connexions
@app.route('/history')
def history():
    connexions = Connexion.query.all()
    return render_template('history.html', connexions=connexions)

if __name__ == '__main__':
    app.run(debug=True)
