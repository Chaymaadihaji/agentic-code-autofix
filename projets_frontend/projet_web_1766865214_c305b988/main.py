from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    history = db.relationship('History', backref='user', lazy=True)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/history')
@login_required
def history():
    history = History.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', history=history)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            msg = MIMEMultipart()
            msg['From'] = 'your_email@example.com'
            msg['To'] = email
            msg['Subject'] = 'Réinitialisation de mot de passe'
            body = 'Veuillez cliquer sur le lien suivant pour réinitialiser votre mot de passe: http://localhost:5000/reset_password/' + user.id
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('your_smtp_server', 587)
            server.starttls()
            server.login(msg['From'], 'your_password')
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            return 'Un email a été envoyé pour réinitialiser votre mot de passe'
    return render_template('forgot_password.html')

@app.route('/reset_password/<id>', methods=['GET', 'POST'])
def reset_password(id):
    if request.method == 'POST':
        password = request.form['password']
        user = User.query.get(id)
        if user:
            user.password = generate_password_hash(password)
            db.session.commit()
            return 'Mot de passe mis à jour'
    return render_template('reset_password.html')

@app.before_request
def before_request():
    if not current_user.is_authenticated and request.path != '/login' and request.path != '/register' and request.path != '/forgot_password' and request.path != '/reset_password/<id>':
        return redirect(url_for('login'))

@app.after_request
def after_request(response):
    if current_user.is_authenticated:
        history = History(user_id=current_user.id, date=datetime.utcnow())
        db.session.add(history)
        db.session.commit()
    return response

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
