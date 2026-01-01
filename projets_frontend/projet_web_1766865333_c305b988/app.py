from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
import smtplib
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    connected_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    history = db.relationship('History', backref='user', lazy=True)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    connected_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

def send_sms(phone_number, code):
    msg = MIMEMultipart()
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = phone_number
    msg['Subject'] = 'Réinitialisation de mot de passe'
    body = f'Votre code de réinitialisation est : {code}'
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], 'your_password')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if validate_email(email):
            if password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user = User(email=email, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash('Les mots de passe ne correspondent pas')
        else:
            flash('Email non valide')
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        if validate_email(email):
            user = User.query.filter_by(email=email).first()
            if user:
                code = generate_code()
                send_sms(user.email, code)
                user.code = code
                db.session.commit()
                return redirect(url_for('reset_password', email=email))
            else:
                flash('Cet email n\'est pas enregistré')
        else:
            flash('Email non valide')
    return render_template('forgot_password.html')

@app.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    if request.method == 'POST':
        code = request.form['code']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if code == User.query.filter_by(email=email).first().code:
            if new_password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                User.query.filter_by(email=email).first().password = hashed_password
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash('Les mots de passe ne correspondent pas')
        else:
            flash('Code de réinitialisation incorrect')
    return render_template('reset_password.html', email=email)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
