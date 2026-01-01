from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from fpdf import FPDF

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibliotheque.db'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)

class Membre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
    membre_id = db.Column(db.Integer, db.ForeignKey('membre.id'), nullable=False)

class FormLivre:
    def __init__(self):
        self.titre = ''
        self.auteur = ''

    def validate(self):
        if not self.titre or not self.auteur:
            return False
        return True

    def save(self):
        livre = Livre(titre=self.titre, auteur=self.auteur)
        db.session.add(livre)
        db.session.commit()

class FormMembre:
    def __init__(self):
        self.nom = ''
        self.prenom = ''

    def validate(self):
        if not self.nom or not self.prenom:
            return False
        return True

    def save(self):
        membre = Membre(nom=self.nom, prenom=self.prenom)
        db.session.add(membre)
        db.session.commit()

class FormEmprunt:
    def __init__(self):
        self.livre_id = ''
        self.membre_id = ''

    def validate(self):
        if not self.livre_id or not self.membre_id:
            return False
        return True

    def save(self):
        emprunt = Emprunt(livre_id=self.livre_id, membre_id=self.membre_id)
        db.session.add(emprunt)
        db.session.commit()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401

@app.route('/livres', methods=['GET'])
@jwt_required
def get_livres():
    livres = Livre.query.all()
    return jsonify([{'id': livre.id, 'titre': livre.titre, 'auteur': livre.auteur} for livre in livres]), 200

@app.route('/livres', methods=['POST'])
@jwt_required
def create_livre():
    form = FormLivre()
    form.titre = request.json.get('titre')
    form.auteur = request.json.get('auteur')
    if form.validate():
        form.save()
        return jsonify({'msg': 'Livre créé avec succès'}), 201
    return jsonify({'msg': 'Formulaire invalide'}), 400

@app.route('/membres', methods=['GET'])
@jwt_required
def get_membres():
    membres = Membre.query.all()
    return jsonify([{'id': membre.id, 'nom': membre.nom, 'prenom': membre.prenom} for membre in membres]), 200

@app.route('/membres', methods=['POST'])
@jwt_required
def create_membre():
    form = FormMembre()
    form.nom = request.json.get('nom')
    form.prenom = request.json.get('prenom')
    if form.validate():
        form.save()
        return jsonify({'msg': 'Membre créé avec succès'}), 201
    return jsonify({'msg': 'Formulaire invalide'}), 400

@app.route('/emprunts', methods=['GET'])
@jwt_required
def get_emprunts():
    emprunts = Emprunt.query.all()
    return jsonify([{'id': emprunt.id, 'livre_id': emprunt.livre_id, 'membre_id': emprunt.membre_id} for emprunt in emprunts]), 200

@app.route('/emprunts', methods=['POST'])
@jwt_required
def create_emprunt():
    form = FormEmprunt()
    form.livre_id = request.json.get('livre_id')
    form.membre_id = request.json.get('membre_id')
    if form.validate():
        form.save()
        return jsonify({'msg': 'Emprunt créé avec succès'}), 201
    return jsonify({'msg': 'Formulaire invalide'}), 400

if __name__ == "__main__":
    app.run(debug=True)
