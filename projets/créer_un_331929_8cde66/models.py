# models.py
import json
import random

class Citation:
    def __init__(self, id, texte, auteur):
        self.id = id
        self.texte = texte
        self.auteur = auteur

class CitationGenerator:
    def __init__(self, citations):
        self.citations = citations

    def generer_citation(self):
        return random.choice(self.citations)
