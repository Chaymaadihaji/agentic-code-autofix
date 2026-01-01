# app.py
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Liste de mots à deviner
mots = ["chien", "chat", "oiseau", "ourse", "cerf"]

# Choix du mot à deviner
mot_secret = random.choice(mots)

# Nombre de tentatives autorisées
max_tentatives = 6

# Nombre de lettres déjà devinées
lettre_devinées = ["_"] * len(mot_secret)

# Nombre de tentatives restantes
tentatives_restantes = max_tentatives
