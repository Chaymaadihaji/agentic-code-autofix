import streamlit as st
import sqlite3
import jwt
import datetime
from fpdf import FPDF
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# Connexion à la base de données
conn = sqlite3.connect('bibliotheque.db')
c = conn.cursor()

# Création de la table livres
c.execute('''CREATE TABLE IF NOT EXISTS livres
             (id INTEGER PRIMARY KEY, titre TEXT, auteur TEXT, edition TEXT)''')

# Création de la table membres
c.execute('''CREATE TABLE IF NOT EXISTS membres
             (id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, email TEXT, mot_de_passe TEXT)''')

# Création de la table emprunts
c.execute('''CREATE TABLE IF NOT EXISTS emprunts
             (id INTEGER PRIMARY KEY, livre_id INTEGER, membre_id INTEGER, date_emprunt DATE, date_retour DATE)''')

# Fonction de gestion des livres
def gestion_livres():
    c.execute("SELECT * FROM livres")
    livres = c.fetchall()
    return livres

# Fonction de gestion des membres
def gestion_membres():
    c.execute("SELECT * FROM membres")
    membres = c.fetchall()
    return membres

# Fonction de gestion des emprunts
def gestion_emprunts():
    c.execute("SELECT * FROM emprunts")
    emprunts = c.fetchall()
    return emprunts

# Fonction de création de token JWT
def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'user_id': user_id
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Fonction de vérification du token JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Page d'accueil
def page_accueil():
    st.title("Bibliothèque")
    st.write("Bienvenue dans la bibliothèque !")

# Page de gestion des livres
def page_gestion_livres():
    st.title("Gestion des livres")
    livres = gestion_livres()
    st.write("Livres disponibles :")
    for livre in livres:
        st.write(f"{livre[1]} - {livre[2]} - {livre[3]}")

# Page de gestion des membres
def page_gestion_membres():
    st.title("Gestion des membres")
    membres = gestion_membres()
    st.write("Membres disponibles :")
    for membre in membres:
        st.write(f"{membre[1]} {membre[2]} - {membre[3]}")

# Page de gestion des emprunts
def page_gestion_emprunts():
    st.title("Gestion des emprunts")
    emprunts = gestion_emprunts()
    st.write("Emprunts disponibles :")
    for emprunt in emprunts:
        st.write(f"{emprunt[1]} - {emprunt[3]} - {emprunt[4]}")

# Page de connexion
def page_connexion():
    st.title("Connexion")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        c.execute("SELECT * FROM membres WHERE email = ?", (email,))
        membre = c.fetchone()
        if membre and check_password_hash(membre[4], mot_de_passe):
            token = create_token(membre[0])
            st.write(f"Bonjour {membre[1]} {membre[2]} ! Votre token est : {token}")
        else:
            st.write("Identifiant ou mot de passe incorrect")

# Page de création de livre
def page_creation_livre():
    st.title("Création de livre")
    titre = st.text_input("Titre")
    auteur = st.text_input("Auteur")
    edition = st.text_input("Édition")
    if st.button("Créer"):
        c.execute("INSERT INTO livres (titre, auteur, edition) VALUES (?, ?, ?)", (titre, auteur, edition))
        conn.commit()
        st.write("Livre créé avec succès")

# Page de création de membre
def page_creation_membre():
    st.title("Création de membre")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    if st.button("Créer"):
        c.execute("INSERT INTO membres (nom, prenom, email, mot_de_passe) VALUES (?, ?, ?, ?)", (nom, prenom, email, generate_password_hash(mot_de_passe)))
        conn.commit()
        st.write("Membre créé avec succès")

# Page de création d'emprunt
def page_creation_emprunt():
    st.title("Création d'emprunt")
    livre_id = st.selectbox("Sélectionner un livre", [livre[0] for livre in gestion_livres()])
    membre_id = st.selectbox("Sélectionner un membre", [membre[0] for membre in gestion_membres()])
    date_emprunt = st.date_input("Date d'emprunt")
    date_retour = st.date_input("Date de retour")
    if st.button("Créer"):
        c.execute("INSERT INTO emprunts (livre_id, membre_id, date_emprunt, date_retour) VALUES (?, ?, ?, ?)", (livre_id, membre_id, date_emprunt, date_retour))
        conn.commit()
        st.write("Emprunt créé avec succès")

# Fonction de génération de rapports PDF
def generate_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Rapport de la bibliothèque", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Nombre de livres : " + str(len(gestion_livres())), ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Nombre de membres : " + str(len(gestion_membres())), ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Nombre d'emprunts : " + str(len(gestion_emprunts())), ln=True, align='C')
    pdf.output("rapport.pdf")

# Fonction de lancement de l'application
def lancer_application():
    page = st.selectbox("Sélectionner une page", ["Page d'accueil", "Page de gestion des livres", "Page de gestion des membres", "Page de gestion des emprunts", "Page de connexion", "Page de création de livre", "Page de création de membre", "Page de création d'emprunt", "Génération de rapports PDF"])
    if page == "Page d'accueil":
        page_accueil()
    elif page == "Page de gestion des livres":
        page_gestion_livres()
    elif page == "Page de gestion des membres":
        page_gestion_membres()
    elif page == "Page de gestion des emprunts":
        page_gestion_emprunts()
    elif page == "Page de connexion":
        page_connexion()
    elif page == "Page de création de livre":
        page_creation_livre()
    elif page == "Page de création de membre":
        page_creation_membre()
    elif page == "Page de création d'emprunt":
        page_creation_emprunt()
    elif page == "Génération de rapports PDF":
        generate_report()

# Lancement de l'application
if __name__ == "__main__":
    lancer_application()
