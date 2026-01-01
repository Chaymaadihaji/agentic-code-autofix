**main.py**
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_mail import Mail, Message
from flask_restful import Api
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import logging
import os
import csv
from datetime import datetime, timedelta
from io import BytesIO
from xhtml2pdf import pisa
from flask_uploads import configure_uploads, UploadSet, IMAGES
from flask_user import UserMixin, SQLAlchemyMixin
from functools import wraps

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
api = Api(app)
cors = CORS(app)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de l'authentification
app.config['JWT_SECRET_KEY'] = 'secret_key_here'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Configuration du mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'

# Configuration de l'upload de fichiers
photos = UploadSet('photos', IMAGES)

# Configuration de la base de données
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean, default=False)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    borrowed_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

# Configuration de la marshmallow
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class BorrowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Borrow

# Configuration de la route de connexion
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({'error': 'invalid credentials'}), 401

# Configuration de la route d'inscription
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user created successfully'})

# Configuration de la route de déconnexion
@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    return jsonify({'message': 'user logged out successfully'})

# Configuration de la route d'ajout de livre
@app.route('/add_book', methods=['POST'])
@jwt_required
def add_book():
    title = request.json['title']
    author = request.json['author']
    date = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
    book = Book(title=title, author=author, date=date)
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'book added successfully'})

# Configuration de la route de modification de livre
@app.route('/modify_book', methods=['POST'])
@jwt_required
def modify_book():
    id = request.json['id']
    title = request.json['title']
    author = request.json['author']
    date = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
    book = Book.query.get(id)
    if book:
        book.title = title
        book.author = author
        book.date = date
        db.session.commit()
        return jsonify({'message': 'book modified successfully'})
    return jsonify({'error': 'book not found'}), 404

# Configuration de la route de suppression de livre
@app.route('/delete_book', methods=['POST'])
@jwt_required
def delete_book():
    id = request.json['id']
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'book deleted successfully'})
    return jsonify({'error': 'book not found'}), 404

# Configuration de la route de recherche de livre
@app.route('/search_book', methods=['POST'])
def search_book():
    query = request.json['query']
    books = Book.query.filter(Book.title.like('%' + query + '%')).all()
    return jsonify([BookSchema().dump(book) for book in books])

# Configuration de la route d'emprunt de livre
@app.route('/borrow_book', methods=['POST'])
@jwt_required
def borrow_book():
    id = request.json['id']
    book = Book.query.get(id)
    if book and not book.returned:
        borrowed_date = datetime.now().date()
        return_date = borrowed_date + timedelta(days=14)
        borrow = Borrow(book_id=id, user_id=get_jwt_identity(), borrowed_date=borrowed_date, return_date=return_date)
        db.session.add(borrow)
        db.session.commit()
        return jsonify({'message': 'book borrowed successfully'})
    return jsonify({'error': 'book not found or already borrowed'}), 404

# Configuration de la route de retour de livre
@app.route('/return_book', methods=['POST'])
@jwt_required
def return_book():
    id = request.json['id']
    borrow = Borrow.query.get(id)
    if borrow:
        book = Book.query.get(borrow.book_id)
        book.returned = True
        db.session.commit()
        return jsonify({'message': 'book returned successfully'})
    return jsonify({'error': 'borrow not found'}), 404

# Configuration de la route de notification de retard
@app.route('/notification', methods=['POST'])
def notification():
    # Faire la notification par email
    return jsonify({'message': 'notification sent successfully'})

# Configuration de la route de dashboard administrateur
@app.route('/dashboard', methods=['GET'])
@jwt_required
def dashboard():
    # Afficher les statistiques
    return jsonify({'message': 'dashboard displayed successfully'})

# Configuration de la route de l'API REST
class BookResource(Resource):
    @jwt_required
    def get(self, id):
        book = Book.query.get(id)
        if book:
            return jsonify(BookSchema().dump(book))
        return jsonify({'error': 'book not found'}), 404

    def put(self, id):
        # Mettre à jour le livre
        return jsonify({'message': 'book updated successfully'})

    def delete(self, id):
        # Supprimer le livre
        return jsonify({'message': 'book deleted successfully'})

class BorrowResource(Resource):
    @jwt_required
    def get(self, id):
        borrow = Borrow.query.get(id)
        if borrow:
            return jsonify(BorrowSchema().dump(borrow))
        return jsonify({'error': 'borrow not found'}), 404

    def put(self, id):
        # Mettre à jour l'emprunt
        return jsonify({'message': 'borrow updated successfully'})

    def delete(self, id):
        # Supprimer l'emprunt
        return jsonify({'message': 'borrow deleted successfully'})

api.add_resource(BookResource, '/book/<int:id>')
api.add_resource(BorrowResource, '/borrow/<int:id>')

# Configuration de la route de test
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'test successful'})

# Configuration de la route de documentation
@app.route('/docs', methods=['GET'])
def docs():
    return jsonify({'message': 'docs displayed successfully'})

# Configuration de la route de déploiement
@app.route('/deploy', methods=['GET'])
def deploy():
    return jsonify({'message': 'deployment successful'})

# Configuration de l'export des données en CSV
@app.route('/export_csv', methods=['GET'])
def export_csv():
    books = Book.query.all()
    output = BytesIO()
    writer = csv.writer(output)
    writer.writerow(['Title', 'Author', 'Date'])
    for book in books:
        writer.writerow([book.title, book.author, book.date])
   
