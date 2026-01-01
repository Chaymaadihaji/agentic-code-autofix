```python
# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_restful import Api
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_ckeditor import CKEditor
from flask_mail import Mail, Message
from datetime import datetime
from pytz import timezone
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
import os
import csv
import pdfkit
from jinja2 import Template

# Config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'votre_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'votre_mot_de_passe'

# Initialize
db = SQLAlchemy(app)
login_manager = LoginManager(app)
api = Api(app)
ckeditor = CKEditor(app)
mail = Mail(app)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# API Routes
class BookResource(Resource):
    def get(self):
        return {'books': [book.to_dict() for book in Book.query.all()]}

class EmpruntResource(Resource):
    def get(self):
        return {'emprunts': [emprunt.to_dict() for emprunt in Emprunt.query.all()]}

# Dashboard Routes
@app.route('/dashboard')
@login_required
def dashboard():
    statistiques = db.session.query(Book).all()
    return render_template('dashboard.html', statistiques=statistiques)

# API
api.add_resource(BookResource, '/api/books')
api.add_resource(EmpruntResource, '/api/emprunts')

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('inscription.html', form=form)

@app.route('/connexion', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('connexion.html', form=form)

@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('index'))

@app.route('/livres')
@login_required
def livres():
    livres = Book.query.all()
    return render_template('livres.html', livres=livres)

@app.route('/ajouter_livre', methods=['GET', 'POST'])
@login_required
def ajouter_livre():
    if request.method == 'POST':
        book = Book(title=request.form['title'], author=request.form['author'], publication_date=datetime.strptime(request.form['publication_date'], '%Y-%m-%d'))
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('livres'))
    return render_template('ajouter_livre.html')

@app.route('/modifier_livre/<int:book_id>', methods=['GET', 'POST'])
@login_required
def modifier_livre(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.publication_date = datetime.strptime(request.form['publication_date'], '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('livres'))
    return render_template('modifier_livre.html', book=book)

@app.route('/supprimer_livre/<int:book_id>')
@login_required
def supprimer_livre(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('livres'))

@app.route('/rechercher_livre', methods=['GET', 'POST'])
@login_required
def rechercher_livre():
    if request.method == 'POST':
        livres = Book.query.filter(Book.title.like('%' + request.form['recherche'] + '%')).all()
        return render_template('rechercher_livre.html', livres=livres)
    return render_template('rechercher_livre.html')

@app.route('/emprunter/<int:book_id>', methods=['GET', 'POST'])
@login_required
def emprunter(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':
        emprunt = Emprunt(book_id=book_id, user_id=current_user.id, start_date=datetime.now(), end_date=datetime.now() + datetime.timedelta(days=14))
        db.session.add(emprunt)
        db.session.commit()
        return redirect(url_for('livres'))
    return render_template('emprunter.html', book=book)

@app.route('/retourner/<int:emprunt_id>')
@login_required
def retourner(emprunt_id):
    emprunt = Emprunt.query.get(emprunt_id)
    emprunt.end_date = datetime.now()
    db.session.commit()
    return redirect(url_for('livres'))

# Export CSV
@app.route('/export_csv')
@login_required
def export_csv():
    livres = Book.query.all()
    with open('livres.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Titre', 'Auteur', 'Date de publication'])
        for livre in livres:
            writer.writerow([livre.title, livre.author, livre.publication_date])
    return redirect(url_for('download_csv'))

@app.route('/download_csv')
@login_required
def download_csv():
    return send_file('livres.csv', as_attachment=True)

# Export PDF
@app.route('/export_pdf')
@login_required
def export_pdf():
    livres = Book.query.all()
    template = Template('livres.html')
    html = template.render(livres=livres)
    pdfkit.from_string(html, 'livres.pdf')
    return redirect(url_for('download_pdf'))

@app.route('/download_pdf')
@login_required
def download_pdf():
    return send_file('livres.pdf', as_attachment=True)

# Recherche avancée
@app.route('/rechercher_avancee', methods=['GET', 'POST'])
@login_required
def rechercher_avancee():
    if request.method == 'POST':
        livres = Book.query.filter(Book.title.like('%' + request.form['recherche'] + '%')).all()
        return render_template('rechercher_avancee.html', livres=livres)
    return render_template('rechercher_avancee.html')

# Système de recommandation
@app.route('/recommandations')
@login_required
def recommandations():
    livres = Book.query.all()
    recommandations = []
    for livre in livres:
        if livre.user_id == current_user.id:
            recommandations.append(livre)
    return render_template('recommandations.html', recommandations=recommandations)

# Run
if __name__ == '__main__':
    db.create_all()
    app
