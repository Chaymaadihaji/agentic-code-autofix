import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import jwt
from pdfgenerator import PDFGenerator
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

db = sqlite3.connect("bibliotheque.db")
cursor = db.cursor()

# Fonctions d'authentification
def add_user(username, password):
    cursor.execute("INSERT INTO membres (username, password) VALUES (?, ?)", (username, password))
    db.commit()

def authenticate(username, password):
    cursor.execute("SELECT * FROM membres WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone()

# Fonctions de gestion de livres
def add_livre(titre, auteur):
    cursor.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", (titre, auteur))
    db.commit()

def get_livres():
    cursor.execute("SELECT * FROM livres")
    return cursor.fetchall()

# Fonctions de gestion d'emprunts
def add_emprunt(livre_id, membre_id):
    cursor.execute("INSERT INTO emprunts (livre_id, membre_id) VALUES (?, ?)", (livre_id, membre_id))
    db.commit()

def get_emprunts():
    cursor.execute("SELECT * FROM emprunts")
    return cursor.fetchall()

# Fonctions d'authentification
def login():
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        user = authenticate(username, password)
        if user:
            st.write("Bienvenue", user[1])
            return user[0]
        else:
            st.write("Nom d'utilisateur ou mot de passe incorrect")

def main():
    st.title("Gestion de Bibliothèque")
    menu = option_menu(st.sidebar, ["Livres", "Membres", "Emprunts", "Déconnexion"], icons=["book", "user", "briefcase", "door"], menu_icon="cast")
    if menu == "Livres":
        titre = st.text_input("Titre")
        auteur = st.text_input("Auteur")
        if st.button("Ajouter livre"):
            add_livre(titre, auteur)
            st.write("Livre ajouté avec succès")
        livres = get_livres()
        st.write(livres)
    elif menu == "Membres":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Ajouter membre"):
            add_user(username, password)
            st.write("Membre ajouté avec succès")
        membres = get_membres()
        st.write(membres)
    elif menu == "Emprunts":
        livre_id = st.selectbox("Livre", get_livres())
        membre_id = st.selectbox("Membre", get_membres())
        if st.button("Emprunter livre"):
            add_emprunt(livre_id, membre_id)
            st.write("Livre emprunté avec succès")
        emprunts = get_emprunts()
        st.write(emprunts)
    elif menu == "Déconnexion":
        st.write("Au revoir")

if __name__ == "__main__":
    main()
