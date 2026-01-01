from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from flask_email import Email
from flask_sms import SMS
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
email = Email(app)
sms = SMS(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    historique_connexion = db.relationship('HistoriqueConnexion', backref='utilisateur', lazy=True)

    def set_password(self, mot_de_passe):
        self.mot_de_passe = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')

    def check_password(self, mot_de_passe):
        return bcrypt.check_password_hash(self.mot_de_passe, mot_de_passe)

class HistoriqueConnexion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

@login_manager.user_loader
def load_utilisateur(id):
    return Utilisateur.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        mot_de_passe = request.form['mot_de_passe']
        utilisateur = Utilisateur.query.filter_by(username=username).first()
        if utilisateur and utilisateur.check_password(mot_de_passe):
            login_user(utilisateur)
            return redirect(url_for('historique'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        mot_de_passe = request.form['mot_de_passe']
        email = request.form['email']
        utilisateur = Utilisateur(username=username, mot_de_passe=mot_de_passe, email=email)
        utilisateur.set_password(mot_de_passe)
        db.session.add(utilisateur)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form['email']
        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur:
            # Envoi du code de réinitialisation via SMS
            sms.send_code(utilisateur)
            return redirect(url_for('reset_code'))
    return render_template('reset.html')

@app.route('/reset_code', methods=['GET', 'POST'])
def reset_code():
    if request.method == 'POST':
        code = request.form['code']
        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur:
            # Réinitialisation du mot de passe
            utilisateur.mot_de_passe = request.form['new_mdp']
            utilisateur.set_password(utilisateur.mot_de_passe)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('reset_code.html')

@app.route('/historique')
@login_required
def historique():
    historiques = HistoriqueConnexion.query.all()
    return render_template('historique.html', historiques=historiques)

if __name__ == '__main__':
    app.run(debug=True)
