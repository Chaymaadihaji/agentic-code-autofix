# test_rapide_fix.py
import os
import sys

# Ajoute le chemin pour importer tes modules
sys.path.append('.')

from executeur.testeur_app import TesteurApp

print("🧪 Test du correctif...")

# Test avec ton projet Hello World
chemin_projet = r"projets\programme_qui_315524_c8de45"

testeur = TesteurApp()
resultat = testeur.tester_application(chemin_projet)

print(f"\n📊 Résultat final:")
print(f"Succès: {resultat['succes']}")
if resultat['succes']:
    print(f"Sortie: {resultat['sortie'][:100]}")
else:
    print(f"Erreur: {resultat['erreur']}")