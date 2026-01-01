"""
 Module de diagnostic d'application - Version Analyse Statique
Détecte les erreurs de syntaxe et les fichiers manquants sans exécuter le code.
"""

import os
import sys
import re
import ast
import json
import traceback

class TesteurApp:
    def __init__(self):
        pass
    
    def tester_application(self, chemin_projet):
        """
        Analyse le projet et détecte les erreurs potentielles.
        """
        print(f"\n🔍 DIAGNOSTIC: Analyse de {chemin_projet}")
        
        
        try:
            fichiers = os.listdir(chemin_projet)
        except Exception as e:
            return {"succes": False, "erreur": f"Dossier illisible: {e}"}
        
       
        fichiers_py = [f for f in fichiers if f.endswith(".py")]
        if not fichiers_py:
            return {"succes": False, "erreur": "Aucun fichier Python trouvé"}
        
        for nom in ["main.py", "app.py", "run.py", "application.py"]:
            if nom in fichiers_py:
                fichier_principal = nom
                break
        else:
            fichier_principal = fichiers_py[0]
            
        chemin_fichier = os.path.join(chemin_projet, fichier_principal)
        print(f" Cible: {fichier_principal}")

       
        app_type = self._detecter_type_intelligent(chemin_fichier, fichiers)
        
       
        return self._analyser_code_statique(chemin_projet, fichier_principal, app_type)

    def _detecter_type_intelligent(self, chemin_fichier, fichiers_projet):
        """Identifie le framework utilisé par analyse de texte."""
        try:
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                contenu = f.read(3000).lower()
        except:
            return "standard"
        
        if 'import streamlit' in contenu or 'st.' in contenu:
            return "streamlit"
        if 'from flask import' in contenu or 'flask(' in contenu or '@app.route' in contenu:
            return "flask"
        if 'import tkinter' in contenu:
            return "tkinter"
        return "standard"

    def _analyser_code_statique(self, chemin_projet, fichier_principal, app_type):
        """
        Le coeur du module : vérifie la syntaxe et les dépendances locales.
        """
        print(f"  Mode: Analyse statique ({app_type})")
        chemin_fichier = os.path.join(chemin_projet, fichier_principal)
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()

            # --- ÉTAPE A: Vérification des fichiers de données ---
            nb_fichiers_crees = self._verifier_fichiers_manquants(chemin_projet, code)
            if nb_fichiers_crees > 0:
                print(f"{nb_fichiers_crees} fichier(s) de données généré(s) pour éviter les crashs.")

            # --- ÉTAPE B: Vérification de la syntaxe Python ---
            print(f" Vérification de la syntaxe...")
            try:
                ast.parse(code)
                print(" Syntaxe valide")
            except SyntaxError as e:
                print(f" ERREUR SYNTAXE: Ligne {e.lineno}")
                # Affichage du contexte de l'erreur
                lignes = code.split('\n')
                debut = max(0, e.lineno - 3)
                fin = min(len(lignes), e.lineno + 2)
                contexte = ""
                for i in range(debut, fin):
                    prefixe = ">>> " if i + 1 == e.lineno else "    "
                    contexte += f"{i+1:3}: {lignes[i]}\n"
                
                return {
                    "succes": False,
                    "type": app_type,
                    "erreur": f"Erreur de syntaxe: {e.msg}",
                    "details": contexte,
                    "ligne": e.lineno
                }

           
            details_supp = ""
            if app_type == "flask":
                routes = self._analyser_routes_flask(code)
                details_supp = f" - {len(routes)} routes détectées"
                if '/' not in routes:
                    print(" Attention: Pas de route racine (/) détectée.")

            return {
                "succes": True,
                "type": app_type,
                "erreur": None,
                "sortie": f"Analyse réussie{details_supp}.",
                "fichier": fichier_principal
            }

        except Exception as e:
            return {"succes": False, "erreur": f"Erreur d'analyse: {str(e)}"}

    def _analyser_routes_flask(self, code):
        """Extrait les routes Flask par Regex."""
        routes = {}
        matches = re.findall(r'@app\.route\(["\']([^"\']+)["\']', code)
        for route in matches:
            routes[route] = True
        return routes

    def _verifier_fichiers_manquants(self, chemin_projet, code):
        """Détecte les appels à open('data.json') et crée les fichiers si absents."""
       
        json_refs = re.findall(r'["\']([^"\']+\.json)["\']', code)
        json_refs = list(set(json_refs)) 
        
        crees = 0
        for nom_f in json_refs:
            chemin = os.path.join(chemin_projet, nom_f)
            if not os.path.exists(chemin):
                try:
                    os.makedirs(os.path.dirname(chemin), exist_ok=True)
                    exemple = {"status": "success", "data": "Exemple généré"}
                    if "task" in nom_f.lower(): exemple = [{"id": 1, "task": "Exemple"}]
                    
                    with open(chemin, 'w', encoding='utf-8') as f:
                        json.dump(exemple, f, indent=2)
                    crees += 1
                except: pass
        return crees


if __name__ == "__main__":
    import tempfile, shutil
    
 
    dossier = tempfile.mkdtemp()
    test_file = os.path.join(dossier, "app.py")
    
    
    with open(test_file, "w") as f:
        f.write("from flask import Flask\napp = Flask(__name__)\n@app.route('/')\ndef index()\n    return 'Hello'")
        
    testeur = TesteurApp()
    resultat = testeur.tester_application(dossier)
    
    print("\n--- RÉSULTAT DU TEST ---")
    if not resultat["succes"]:
        print(f"Statut:  Erreur trouvée")
        print(f"Message: {resultat['erreur']}")
        print(f"Contexte:\n{resultat.get('details', '')}")
    else:
        print(f"Statut:  Tout est correct")
    
    shutil.rmtree(dossier)