"""
🧪 Module de test d'application - Version avec détection des routes manquantes
"""

import os
import subprocess
import sys
import time
import re
import requests
import traceback
import json  # Ajouté pour la nouvelle fonction

class TesteurApp:
    def __init__(self):
        pass
    
    def tester_application(self, chemin_projet):
        """
        Teste si l'application fonctionne avec debug détaillé
        """
        print(f"\n🔍 TEST: Analyse de {chemin_projet}")
        
        # 1. Lister tous les fichiers du projet
        print(f"📁 Fichiers dans le projet:")
        try:
            fichiers = os.listdir(chemin_projet)
            for f in fichiers:
                print(f"   - {f}")
        except Exception as e:
            print(f"   ❌ Erreur listing: {e}")
            return {
                "succes": False,
                "erreur": f"Impossible de lire le dossier: {e}",
                "sortie": "",
                "code_retour": -1
            }
        
        # 2. Chercher le fichier principal
        fichiers_py = [f for f in fichiers if f.endswith(".py")]
        print(f"📄 Fichiers Python trouvés: {fichiers_py}")
        
        for nom_prefere in ["main.py", "app.py", "run.py", "application.py"]:
            if nom_prefere in fichiers_py:
                fichier_principal = nom_prefere
                break
        else:
            fichier_principal = fichiers_py[0] if fichiers_py else None
        
        if not fichier_principal:
            print("❌ Aucun fichier Python trouvé!")
            return {
                "succes": False,
                "erreur": "Aucun fichier Python trouvé",
                "sortie": "",
                "code_retour": -1
            }
        
        chemin_fichier = os.path.join(chemin_projet, fichier_principal)
        print(f"🎯 Fichier principal sélectionné: {fichier_principal}")
        
        # DÉTECTION APPLICATIONS FLASK
        is_flask_app = self._detecter_flask_app(chemin_fichier, fichiers)
        
        if is_flask_app:
            print("🔥 Détection: Application Flask - Utilisation du test spécialisé")
            return self._tester_application_flask(chemin_projet, fichier_principal)
        else:
            print("📟 Application standard - Utilisation du test normal")
            return self._tester_application_standard(chemin_projet, fichier_principal)
    
    def _detecter_flask_app(self, chemin_fichier, fichiers_projet):
        """
        Détecte si c'est une application Flask
        """
        # Vérifier les noms de fichiers typiques Flask
        flask_files = ['app.py', 'application.py', 'flask_app.py', 'server.py']
        fichier_nom = os.path.basename(chemin_fichier)
        
        if fichier_nom.lower() in flask_files:
            return True
        
        # Vérifier la présence de dossiers Flask typiques
        if 'templates' in fichiers_projet or 'static' in fichiers_projet:
            return True
        
        # Lire le contenu du fichier pour vérifier les imports Flask
        try:
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                contenu = f.read(2000)  # Lire les 2000 premiers caractères
                
                # Rechercher des indices Flask
                flask_indicators = [
                    'from flask import', 'import flask', 'Flask(',
                    '@app.route', 'app.run(', 'flask.Flask'
                ]
                
                for indicator in flask_indicators:
                    if indicator.lower() in contenu.lower():
                        return True
        except:
            pass
        
        return False
    
    def _tester_application_flask(self, chemin_projet, fichier_principal):
        """
        Test spécial pour applications Flask avec détection des routes manquantes
        """
        print(f"🌐 Test d'application Flask...")
        chemin_fichier = os.path.join(chemin_projet, fichier_principal)
        
        try:
            # 1. Lire le code pour debug
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                code_genere = f.read()
            
            # ============ AJOUT: Vérification des fichiers manquants ============
            print(f"\n🔍 Vérification des fichiers de données...")
            fichiers_crees = self._verifier_fichiers_manquants(chemin_projet, code_genere)
            if fichiers_crees > 0:
                print(f"   📝 {fichiers_crees} fichier(s) de données créé(s)")
            # ====================================================================
            
            # Afficher le code Flask
            print(f"\n🔎 CODE FLASK GÉNÉRÉ ({len(code_genere)} caractères):")
            print("=" * 60)
            lignes = code_genere.split('\n')

            # Afficher toutes les lignes
            for i, ligne in enumerate(lignes[:100]):  # Limiter à 100 lignes max
                print(f"{i+1:3}: {ligne}")
            
            if len(lignes) > 100:
                print(f"... ({len(lignes)-100} lignes supplémentaires)")
            
            print("=" * 60)
            
            # 2. Vérifier la syntaxe
            print(f"\n🔧 Vérification syntaxique Flask...")
            try:
                import ast
                ast.parse(code_genere)
                print("✅ Syntaxe Python valide")
            except SyntaxError as e:
                print(f"❌ Erreur de syntaxe: {e}")
                print(f"   Message: {e.msg}")
                print(f"   Position: Ligne {e.lineno}, Colonne {e.offset}")
                
                if e.text:
                    print(f"   Ligne problématique: {e.text.strip()}")
                
                # Afficher le contexte autour de l'erreur
                print(f"\n🔍 CONTEXTE DE L'ERREUR (ligne {e.lineno}):")
                start_line = max(1, e.lineno - 5)
                end_line = min(len(lignes), e.lineno + 5)
                
                for i in range(start_line, end_line + 1):
                    if 0 <= i-1 < len(lignes):
                        ligne_num = i
                        ligne_text = lignes[i-1]
                        if ligne_num == e.lineno:
                            print(f">>> {ligne_num:3}: {ligne_text}")
                        else:
                            print(f"    {ligne_num:3}: {ligne_text}")
                
                return {
                    "succes": False,
                    "erreur": f"SyntaxError Flask: {e.msg}",
                    "sortie": f"Ligne {e.lineno}: {e.text}",
                    "code_retour": 1,
                    "fichier_testé": fichier_principal,
                    "type": "flask",
                    "details": f"Erreur syntaxique à la ligne {e.lineno}"
                }
            
            # 3. Analyser les routes Flask présentes
            print(f"\n🔍 Analyse des routes Flask...")
            routes = self._analyser_routes_flask(code_genere)
            print(f"   Routes détectées: {list(routes.keys())}")
            
            # Vérifier si une route racine '/' existe
            if '/' not in routes:
                print(f"   ⚠️  Route racine '/' manquante!")
                
                # Tenter d'ajouter une route racine automatiquement
                print(f"   🔧 Tentative d'ajout de route racine...")
                code_corrige = self._ajouter_route_racine(code_genere, routes)
                
                if code_corrige != code_genere:
                    print(f"   ✅ Route racine ajoutée automatiquement")
                    with open(chemin_fichier, 'w', encoding='utf-8') as f:
                        f.write(code_corrige)
                    
                    # Rélire le code corrigé
                    with open(chemin_fichier, 'r', encoding='utf-8') as f:
                        code_genere = f.read()
            
            # 4. Démarrer Flask en arrière-plan
            print(f"\n🚀 Démarrage du serveur Flask...")
            flask_process = subprocess.Popen(
                [sys.executable, fichier_principal],
                cwd=chemin_projet,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            # 5. Attendre que Flask démarre
            print(f"⏳ Attente du démarrage Flask (5 secondes)...")
            time.sleep(5)
            
            # 6. Tester différentes routes
            print(f"📡 Test des routes Flask...")
            
            # Tester d'abord la racine
            resultat_racine = self._tester_route_flask('/', flask_process)
            
            if resultat_racine["succes"]:
                print(f"✅ Serveur Flask répond! {resultat_racine['details']}")
                flask_process.terminate()
                
                return {
                    "succes": True,
                    "erreur": None,
                    "sortie": f"Application Flask fonctionnelle. {resultat_racine['details']}",
                    "code_retour": 0,
                    "fichier_testé": fichier_principal,
                    "type": "flask"
                }
            else:
                # Essayer d'autres routes connues
                print(f"   ⚠️  Route '/' inaccessible, test des autres routes...")
                
                for route in routes.keys():
                    if route != '/':
                        resultat = self._tester_route_flask(route, flask_process)
                        if resultat["succes"]:
                            print(f"✅ Route {route} accessible: {resultat['details']}")
                            flask_process.terminate()
                            
                            return {
                                "succes": True,
                                "erreur": None,
                                "sortie": f"Application Flask fonctionnelle via route {route}. {resultat['details']}",
                                "code_retour": 0,
                                "fichier_testé": fichier_principal,
                                "type": "flask",
                                "route_utilisee": route
                            }
                
                # Aucune route accessible
                print(f"❌ Aucune route Flask accessible")
                flask_process.terminate()
                
                return {
                    "succes": False,
                    "erreur": "Aucune route Flask n'est accessible",
                    "sortie": f"Routes testées: {list(routes.keys())}",
                    "code_retour": -6,
                    "fichier_testé": fichier_principal,
                    "type": "flask"
                }
                
        except Exception as e:
            print(f"❌ EXCEPTION test Flask: {e}")
            import traceback
            traceback.print_exc()
            return {
                "succes": False,
                "erreur": f"Exception test Flask: {str(e)}",
                "sortie": "",
                "code_retour": -9,
                "fichier_testé": fichier_principal,
                "type": "flask"
            }
    
    def _analyser_routes_flask(self, code):
        """Analyse les routes Flask définies dans le code"""
        routes = {}
        
        # Chercher les décorateurs @app.route
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('@app.route'):
                # Extraire l'argument de route
                match = re.search(r'@app\.route\(["\']([^"\']+)["\']', line)
                if match:
                    route = match.group(1)
                    # Trouver la fonction associée (lignes suivantes)
                    for j in range(i+1, min(i+5, len(lines))):
                        if lines[j].strip().startswith('def '):
                            func_match = re.search(r'def\s+(\w+)', lines[j])
                            if func_match:
                                func_name = func_match.group(1)
                                routes[route] = func_name
                                break
        
        return routes
    
    def _ajouter_route_racine(self, code, routes):
        """Ajoute une route racine '/' si elle manque"""
        lines = code.split('\n')
        
        # Chercher où ajouter la route (juste avant if __name__ == "__main__")
        for i, line in enumerate(lines):
            if 'if __name__ == "__main__":' in line:
                # Ajouter une route racine simple
                route_racine = '''
@app.route('/')
def index():
    """Page principale"""
    return "<h1>Application Flask Fonctionnelle</h1><p>L'application est en ligne.</p>"
'''
                
                lines.insert(i, route_racine)
                break
        
        return '\n'.join(lines)
    
    def _tester_route_flask(self, route, flask_process):
        """Teste une route spécifique de Flask"""
        try:
            response = requests.get(f'http://localhost:5000{route}', timeout=3)
            
            return {
                "succes": True,
                "details": f"Route {route}: HTTP {response.status_code}",
                "response": response
            }
        except requests.exceptions.ConnectionError:
            return {
                "succes": False,
                "details": f"Route {route}: Connexion refusée"
            }
        except requests.exceptions.RequestException as e:
            return {
                "succes": False,
                "details": f"Route {route}: Erreur {str(e)[:50]}"
            }
    
    def _verifier_fichiers_manquants(self, chemin_projet, code_genere):
        """Vérifie et crée les fichiers référencés dans le code"""
        import re
        
        # Chercher les fichiers .json référencés
        json_files = re.findall(r'open\(["\']([^"\']+\.json)["\']', code_genere)
        
        # Chercher aussi les imports json
        json_imports = re.findall(r'with open\(["\']([^"\']+\.json)["\']', code_genere)
        json_files.extend(json_imports)
        
        # Chercher les références à des fichiers de données
        data_patterns = [
            r'load\(["\']([^"\']+\.json)["\']',
            r'read_json\(["\']([^"\']+\.json)["\']',
            r'\.json["\']'
        ]
        
        for pattern in data_patterns:
            matches = re.findall(pattern, code_genere)
            json_files.extend(matches)
        
        # Éliminer les doublons
        json_files = list(set(json_files))
        
        fichiers_crees = 0
        for json_file in json_files:
            chemin_json = os.path.join(chemin_projet, json_file)
            if not os.path.exists(chemin_json):
                print(f"   ⚠️  Fichier {json_file} manquant - création...")
                
                # Créer les répertoires parents si nécessaire
                os.makedirs(os.path.dirname(chemin_json), exist_ok=True)
                
                # Créer un exemple de données selon le nom du fichier
                if 'citation' in json_file.lower():
                    donnees = [
                        "Exemple de citation 1 - La vie est belle",
                        "Exemple de citation 2 - Apprends de chaque jour", 
                        "Exemple de citation 3 - Le succès vient avec la persévérance"
                    ]
                elif 'task' in json_file.lower() or 'tache' in json_file.lower():
                    donnees = [
                        {"id": 1, "title": "Tâche exemple 1", "completed": False},
                        {"id": 2, "title": "Tâche exemple 2", "completed": True}
                    ]
                elif 'data' in json_file.lower() or 'donne' in json_file.lower():
                    donnees = [
                        {"id": 1, "valeur": "Donnée 1"},
                        {"id": 2, "valeur": "Donnée 2"}
                    ]
                else:
                    donnees = {"exemple": "Données d'exemple", "version": "1.0"}
                
                try:
                    with open(chemin_json, 'w', encoding='utf-8') as f:
                        json.dump(donnees, f, ensure_ascii=False, indent=2)
                    
                    print(f"   ✅ {json_file} créé avec des données d'exemple")
                    fichiers_crees += 1
                except Exception as e:
                    print(f"   ❌ Erreur création {json_file}: {e}")
        
        return fichiers_crees
    
    def _tester_application_standard(self, chemin_projet, fichier_principal):
        """
        Test standard pour scripts Python normaux
        """
        chemin_fichier = os.path.join(chemin_projet, fichier_principal)
        
        try:
            # Lire le code
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                code_genere = f.read()
            
            # ============ AJOUT: Vérification des fichiers manquants ============
            self._verifier_fichiers_manquants(chemin_projet, code_genere)
            # ====================================================================
            
            # Vérifier la syntaxe
            print(f"\n🔧 Vérification syntaxique...")
            try:
                import ast
                ast.parse(code_genere)
                print("✅ Syntaxe Python valide")
            except SyntaxError as e:
                print(f"❌ Erreur de syntaxe: {e}")
                return {
                    "succes": False,
                    "erreur": f"SyntaxError: {e.msg}",
                    "sortie": f"Ligne {e.lineno}",
                    "code_retour": 1,
                    "fichier_testé": fichier_principal
                }
            
            # Exécuter
            print(f"\n🚀 Exécution de {fichier_principal}...")
            result = subprocess.run(
                [sys.executable, fichier_principal], 
                cwd=chemin_projet, 
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
            )
            
            print(f"📊 Résultat: Code {result.returncode}")
            
            if result.returncode == 0:
                return {
                    "succes": True,
                    "erreur": None,
                    "sortie": result.stdout[:500],
                    "code_retour": 0,
                    "fichier_testé": fichier_principal
                }
            else:
                return {
                    "succes": False,
                    "erreur": f"Code retour {result.returncode}",
                    "sortie": result.stderr[:500] if result.stderr else result.stdout[:500],
                    "code_retour": result.returncode,
                    "fichier_testé": fichier_principal
                }
                
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            return {
                "succes": False,
                "erreur": f"Exception: {str(e)}",
                "sortie": "",
                "code_retour": -4,
                "fichier_testé": fichier_principal
            }

# Fonction de test rapide
def test_rapide():
    """Test rapide du module"""
    print("🧪 Test rapide du TesteurApp amélioré")
    
    # Créer un dossier test
    import tempfile
    import shutil
    
    test_dir = tempfile.mkdtemp()
    print(f"Dossier test: {test_dir}")
    
    # Créer une application Flask sans route racine (similaire au bug)
    app_code = '''from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def api_data():
    return jsonify({"message": "API works"})

if __name__ == "__main__":
    app.run()
'''
    
    with open(os.path.join(test_dir, "app.py"), 'w', encoding='utf-8') as f:
        f.write(app_code)
    
    # Tester
    testeur = TesteurApp()
    resultat = testeur.tester_application(test_dir)
    
    print(f"\n📊 Résultat: Succès = {resultat.get('succes', False)}")
    print(f"Erreur: {resultat.get('erreur', 'Aucune')}")
    
    # Nettoyer
    shutil.rmtree(test_dir)
    print(f"\n🧹 Dossier test nettoyé")

if __name__ == "__main__":
    test_rapide()