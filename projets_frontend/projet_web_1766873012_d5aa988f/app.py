python
# app.py

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from io import BytesIO
from fpdf import FPDF
from datetime import datetime, timedelta
import sqlite3
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'votre_email'
app.config['MAIL_PASSWORD'] = 'votre_mot_de_passe'

db = SQLAlchemy(app)
mail = Mail(app)
api = Api(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connecter')

class RegisterForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Inscrire')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/books')
@login_required
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        book = Book(title=title, author=author, user_id=current_user.id)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/modify_book/<int:id>', methods=['GET', 'POST'])
@login_required
def modify_book(id):
    book = Book.query.get(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('modify_book.html', book=book)

@app.route('/delete_book/<int:id>')
@login_required
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books'))

@app.route('/borrow_book/<int:id>')
@login_required
def borrow_book(id):
    book = Book.query.get(id)
    if book.user_id is None:
        book.user_id = current_user.id
        book.date_borrowed = datetime.now()
        book.date_returned = datetime.now() + timedelta(days=14)
        db.session.commit()
        return redirect(url_for('books'))
    return 'Le livre est déjà emprunté'

@app.route('/return_book/<int:id>')
@login_required
def return_book(id):
    book = Book.query.get(id)
    if book.user_id == current_user.id:
        book.user_id = None
        book.date_returned = datetime.now()
        db.session.commit()
        return redirect(url_for('books'))
    return 'Vous n\'avez pas emprunté ce livre'

@app.route('/search_books', methods=['GET', 'POST'])
@login_required
def search_books():
    if request.method == 'POST':
        query = request.form['query']
        books = Book.query.filter(Book.title.like('%' + query + '%')).all()
        return render_template('search_books.html', books=books)
    return render_template('search_books.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        books = Book.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', books=books)
    return 'Vous n\'êtes pas connecté'

@app.route('/export_csv')
@login_required
def export_csv():
    books = Book.query.all()
    output = BytesIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Author', 'User ID', 'Date Borrowed', 'Date Returned'])
    for book in books:
        writer.writerow([book.title, book.author, book.user_id, book.date_borrowed, book.date_returned])
    output.seek(0)
    return send_file(output, as_attachment=True, attachment_filename='books.csv')

@app.route('/export_pdf')
@login_required
def export_pdf():
    books = Book.query.all()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Liste des livres', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    for book in books:
        pdf.cell(200, 10, txt=book.title + ' - ' + book.author, ln=True, align='L')
    pdf.output('books.pdf')
    return send_file('books.pdf', as_attachment=True)

class BookResource(Resource):
    def get(self, id):
        book = Book.query.get(id)
        if book:
            return {'title': book.title, 'author': book.author}
        return {'error': 'Livre non trouvé'}

class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [{'title': book.title, 'author': book.author, 'id': book.id} for book in books]

class BorrowBookResource(Resource):
    def post(self, id):
        book = Book.query.get(id)
        if book:
            book.user_id = current_user.id
            book.date_borrowed = datetime.now()
            book.date_returned = datetime.now() + timedelta(days=14)
            db.session.commit()
            return {'message': 'Le livre a été emprunté'}
        return {'error': 'Livre non trouvé'}

class ReturnBookResource(Resource):
    def post(self, id):
        book = Book.query.get(id)
        if book:
            book.user_id = None
            book.date_returned = datetime.now()
            db.session.commit()
            return {'message': 'Le livre a été retourné'}
        return {'error': 'Livre non trouvé'}

api.add_resource(BookResource, '/book/<int:id>')
api.add_resource(BookListResource, '/books')
api.add_resource(BorrowBookResource, '/borrow_book/<int:id>')
api.add_resource(ReturnBookResource, '/return_book/<int:id>')

@app.errorhandler(404)
def page_not_found(e):
    return 'Page non trouvée'

@app.errorhandler(500)
def internal_server_error(e):
    return 'Erreur interne du serveur'

@app.route('/send_email')
@login_required
def send_email():
    msg = Message('Test email', sender='votre_email', recipients=['destinataire_email'])
    msg.body = 'Ceci est un test d\'email'
    mail.send(msg)
    return 'Email envoyé'

@app.route('/test')
def test():
    return 'Test réussi'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
