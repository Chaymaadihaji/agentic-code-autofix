# app.py

import os
import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bootstrap4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bootstrap = Bootstrap(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fiches_patients = db.relationship('FichePatient', backref='user', lazy=True)

class FichePatient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64), nullable=False)
    patient_age = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Ordonnance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('fiche_patient.id'), nullable=False)
    medicament = db.Column(db.String(64), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('fiche_patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    heure = db.Column(db.String(64), nullable=False)

class AlerteMedicament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicament = db.Column(db.String(64), nullable=False)
    alerte = db.Column(db.Boolean, nullable=False)

class DossierMedical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('fiche_patient.id'), nullable=False)
    dossier = db.Column(db.Text, nullable=False)

class GraphiqueSuiviSante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('fiche_patient.id'), nullable=False)
    valeur = db.Column(db.Float, nullable=False)

class RapportMedicin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('fiche_patient.id'), nullable=False)
    rapport = db.Column(db.Text, nullable=False)

class FormulaireFichePatient(FlaskForm):
    patient_name = StringField('Nom du patient', validators=[DataRequired()])
    patient_age = StringField('Age du patient', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class FormulaireOrdonnance(FlaskForm):
    medicament = StringField('Medicament', validators=[DataRequired()])
    quantite = StringField('Quantite', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class FormulaireRendezVous(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    heure = StringField('Heure', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class FormulaireAlerteMedicament(FlaskForm):
    medicament = StringField('Medicament', validators=[DataRequired()])
    alerte = StringField('Alerte', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class FormulaireDossierMedical(FlaskForm):
    dossier = StringField('Dossier', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class FormulaireGraphiqueSuiviSante(FlaskForm):
    valeur = StringField('Valeur', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class FormulaireRapportMedicin(FlaskForm):
    rapport = StringField('Rapport', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fiche_patient', methods=['GET', 'POST'])
def fiche_patient():
    form = FormulaireFichePatient()
    if form.validate_on_submit():
        patient_name = form.patient_name.data
        patient_age = form.patient_age.data
        fiche_patient = FichePatient(patient_name=patient_name, patient_age=patient_age, user_id=current_user.id)
        db.session.add(fiche_patient)
        db.session.commit()
        return redirect(url_for('fiche_patient'))
    return render_template('fiche_patient.html', form=form)

@app.route('/ordonnance', methods=['GET', 'POST'])
def ordonnance():
    form = FormulaireOrdonnance()
    if form.validate_on_submit():
        medicament = form.medicament.data
        quantite = form.quantite.data
        ordonnance = Ordonnance(medicament=medicament, quantite=quantite, patient_id=current_user.fiches_patients[-1].id)
        db.session.add(ordonnance)
        db.session.commit()
        return redirect(url_for('ordonnance'))
    return render_template('ordonnance.html', form=form)

@app.route('/rendez_vous', methods=['GET', 'POST'])
def rendez_vous():
    form = FormulaireRendezVous()
    if form.validate_on_submit():
        date = form.date.data
        heure = form.heure.data
        rendez_vous = RendezVous(date=date, heure=heure, patient_id=current_user.fiches_patients[-1].id)
        db.session.add(rendez_vous)
        db.session.commit()
        return redirect(url_for('rendez_vous'))
    return render_template('rendez_vous.html', form=form)

@app.route('/alerte_medicament', methods=['GET', 'POST'])
def alerte_medicament():
    form = FormulaireAlerteMedicament()
    if form.validate_on_submit():
        medicament = form.medicament.data
        alerte = form.alerte.data
        alerte_medicament = AlerteMedicament(medicament=medicament, alerte=alerte)
        db.session.add(alerte_medicament)
        db.session.commit()
        return redirect(url_for('alerte_medicament'))
    return render_template('alerte_medicament.html', form=form)

@app.route('/dossier_medical', methods=['GET', 'POST'])
def dossier_medical():
    form = FormulaireDossierMedical()
    if form.validate_on_submit():
        dossier = form.dossier.data
        dossier_medical = DossierMedical(dossier=dossier, patient_id=current_user.fiches_patients[-1].id)
        db.session.add(dossier_medical)
        db.session.commit()
        return redirect(url_for('dossier_medical'))
    return render_template('dossier_medical.html', form=form)

@app.route('/graphique_suivi_sante', methods=['GET', 'POST'])
def graphique_suivi_sante():
    form = FormulaireGraphiqueSuiviSante()
    if form.validate_on_submit():
        valeur = form.valeur.data
        graphique_suivi_sante = GraphiqueSuiviSante(valeur=valeur, patient_id=current_user.fiches_patients[-1].id)
        db.session.add(graphique_suivi_sante)
        db.session.commit()
        return redirect(url_for('graphique_suivi_sante'))
    return render_template('graphique_suivi_sante.html', form=form)

@app.route('/rapport_medicin', methods=['GET', 'POST'])
def rapport_medicin():
    form = FormulaireRapportMedicin()
    if form.validate_on_submit():
        rapport = form.rapport.data
        rapport_medicin = RapportMedicin(rapport=rapport, patient_id=current_user.fiches_patients[-1].id)
        db.session.add(rapport_medicin)
        db.session.commit()
        return redirect(url_for('rapport_medicin'))
    return render_template('rapport_medicin.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
