python
# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Book', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    edition = db.Column(db.String(64), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    borrowed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    borrowed_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    borrowed = db.Column(db.Boolean, default=False)
    return_status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Book {self.title}>'

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrowed_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    returned = db.Column(db.Boolean, default=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    sent = db.Column(db.Boolean, default=False)

def send_email(to, subject, body):
    sender_email = current_app.config['MAIL_SERVER']
    sender_password = current_app.config['MAIL_PASSWORD']
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, to, text)
    server.quit()

def overdue_books():
    now = datetime.datetime.now()
    overdue = []
    for book in Book.query.all():
        if book.borrowed and book.return_date < now:
            overdue.append(book)
    return overdue

def get_stats():
    users = User.query.count()
    books = Book.query.count()
    borrowed_books = Borrow.query.filter_by(returned=False).count()
    overdue_books_count = overdue_books().count()
    return {
        'users': users,
        'books': books,
        'borrowed_books': borrowed_books,
        'overdue_books': overdue_books_count
    }
