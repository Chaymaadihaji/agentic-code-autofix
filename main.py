#!/usr/bin/env python3
"""
🤖 ROBOT DÉVELOPPEUR - Point d'entrée principal
Version avec gestion automatique backend + frontend
"""

import os
import sys
import time
import json
from dotenv import load_dotenv
from correcteur.validateur import ValidateurApplication

# CHARGER .env AVANT TOUT
load_dotenv()

# VÉRIFIER SI LA CLÉ API EST PRÉSENTE
if not os.getenv("GROQ_API_KEY"):
    print("❌ ERREUR : GROQ_API_KEY non trouvée dans .env")
    print("Assure-toi d'avoir un fichier .env avec :")
    print("GROQ_API_KEY=ta_cle_api_ici")
    print("LLM_MODEL=llama-3.3-70b-versatile")
    sys.exit(1)

print(f"✅ Clé API chargée : {os.getenv('GROQ_API_KEY')[:10]}...")

# Import des modules
try:
    from cerveau.analyseur import Analyser
    from cerveau.architecte import Architecte
    from cerveau.planificateur import Planificateur
    from executeur.createur_fichiers import CreateurFichiers
    from executeur.redacteur_code import RedacteurCode
    from executeur.gestionnaire_deps import GestionnaireDeps
    from executeur.testeur_app import TesteurApp
    from correcteur.detecteur_bugs import DetecteurBugs
    from correcteur.auto_reparateur import AutoReparateur
    from correcteur.apprentissage import Apprentissage
except ImportError as e:
    print(f"❌ Erreur d'importation : {e}")
    print("Vérifie que tous les fichiers Python existent")
    sys.exit(1)

class RobotDeveloppeur:
    def __init__(self):
        """Initialise tous les composants du robot"""
        print("🤖 Initialisation du Robot Développeur...")
        
        try:
            # Modules cerveau
            self.analyseur = Analyser()
            self.architecte = Architecte()
            self.planificateur = Planificateur()
            
            # Modules exécuteur
            self.createur = CreateurFichiers()
            self.redacteur = RedacteurCode()
            self.gestionnaire_deps = GestionnaireDeps()
            self.testeur = TesteurApp()
            
            # Modules correcteur
            self.detecteur = DetecteurBugs()
            self.reparateur = AutoReparateur()
            self.apprentissage = Apprentissage()
            
            # Configuration
            self.max_tentatives = int(os.getenv("MAX_TENTATIVES", 5))
            self.validateur = ValidateurApplication()
            
            print("✅ Tous les modules initialisés avec succès")
            
        except Exception as e:
            print(f"❌ Erreur d'initialisation : {e}")
            print("Vérifie ta clé API et ta connexion internet")
            sys.exit(1)
    
    def demarrer(self, demande_utilisateur=None):
        """Point d'entrée principal - alias pour executer_demande"""
        # Si aucune demande fournie, demander interactivement
        if demande_utilisateur is None:
            demande_utilisateur = input("\n📝 Que veux-tu que je développe ?\n> ")
        
        return self.executer_demande(demande_utilisateur)
    
    def executer_demande(self, demande_utilisateur):
        """Exécute une demande de développement COMPLÈTE (backend + frontend)"""
        if not demande_utilisateur or not demande_utilisateur.strip():
            print("❌ Aucune demande valide fournie.")
            return {"succes": False, "chemin": "", "tentatives": 0}
        
        # Nettoyer la demande
        demande_utilisateur = demande_utilisateur.strip('"\'')
        
        print(f"\n📝 Demande : {demande_utilisateur}")
        print("-" * 50)
        
        # 1. ANALYSE COMPLÈTE DE LA DEMANDE
        print("🧠 Phase 1 : Analyse intelligente de la demande...")
        analyse = self.analyseur.analyser_demande(demande_utilisateur)
        
        print(f"   → Type d'application: {analyse.get('type_application', 'inconnu')}")
        print(f"   → Interface nécessaire: {'✅ OUI' if analyse.get('besoin_interface', False) else '❌ NON'}")
        
        if analyse.get('besoin_interface', False):
            print(f"   → Type interface: {analyse.get('type_interface', 'inconnu')}")
            print(f"   → Composants UI: {analyse.get('composants_ui_attendus', [])}")
        
        # 2. ARCHITECTURE ADAPTÉE (backend + frontend si nécessaire)
        print("\n🏗️ Phase 2 : Conception de l'architecture COMPLÈTE...")
        architecture = self.architecte.creer_architecture(analyse)
        
        print(f"   → Fichiers à créer: {len(architecture.get('fichiers', []))}")
        print(f"   → Structure de dossiers: {architecture.get('structure_dossiers', [])}")
        
        # 3. PLANIFICATION
        print("\n📋 Phase 3 : Planification des étapes...")
        plan = self.planificateur.creer_plan(analyse, architecture)
        
        # 4. CRÉATION DU PROJET
        print("\n📁 Phase 4 : Création de la structure COMPLÈTE...")
        nom_projet = self._generer_nom_projet(demande_utilisateur)
        chemin_projet = os.path.join("projets", nom_projet)
        
        # Créer la structure complète (backend + frontend)
        self._creer_structure_complete(chemin_projet, architecture, demande_utilisateur, analyse)
        print(f"   → Projet créé: {chemin_projet}")
        
        # 5. BOUCLE DE GÉNÉRATION/TEST/CORRECTION
        succes, tentatives_effectuees = self._boucle_generation_test(
            chemin_projet, architecture, demande_utilisateur, analyse
        )
        
        # 6. RAPPORT FINAL
        self._generer_rapport_final(
            chemin_projet, demande_utilisateur, tentatives_effectuees, succes, analyse
        )
        
        return {
            'succes': succes,
            'chemin': chemin_projet,
            'tentatives': tentatives_effectuees,
            'analyse': analyse
        }
    
    def _creer_structure_complete(self, chemin_projet, architecture, demande, analyse):
        """Crée TOUTE la structure du projet (backend + frontend)"""
        print("   📂 Création de la structure complète...")
        
        # Créer le dossier principal
        os.makedirs(chemin_projet, exist_ok=True)
        
        # Créer tous les sous-dossiers
        for dossier in architecture.get("structure_dossiers", []):
            dossier_path = os.path.join(chemin_projet, dossier)
            os.makedirs(dossier_path, exist_ok=True)
            print(f"      → Dossier: {dossier}")
        
        # Sauvegarder la demande originale
        with open(os.path.join(chemin_projet, "demande.txt"), "w", encoding="utf-8") as f:
            f.write(demande)
        
        # Sauvegarder l'analyse technique
        with open(os.path.join(chemin_projet, "analyse_technique.json"), "w", encoding="utf-8") as f:
            json.dump(analyse, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Structure créée: {chemin_projet}")
    
    def _boucle_generation_test(self, chemin_projet, architecture, demande, analyse):
        """Boucle complète de génération et test"""
        succes = False
        tentatives_effectuees = 0
        
        for tentative in range(1, self.max_tentatives + 1):
            tentatives_effectuees = tentative
            print(f"\n🔄 Tentative {tentative}/{self.max_tentatives}")
            
            # ÉTAPE CRUCIALE : GÉNÉRER TOUS LES FICHIERS (backend + frontend)
            print("   📄 Génération de TOUS les fichiers...")
            
            for fichier_info in architecture.get('fichiers', []):
                nom_fichier = fichier_info['nom']
                print(f"      ✍️  {nom_fichier}")
                
                # GÉNÉRER LE CODE ADAPTÉ (backend OU frontend)
                code = self.redacteur.generer_code_adapte(
                    demande, 
                    fichier_info, 
                    analyse,
                    chemin_projet
                )
                
                # Écrire le fichier
                self.createur.ecrire_fichier(chemin_projet, nom_fichier, code)
            
            # AJOUTEZ ICI LA CORRECTION DES IMPORTS
            print("   🔧 Correction automatique des imports...")
            self._corriger_imports_flask(chemin_projet)
            
            # Installer les dépendances (seulement à la première tentative)
            if tentative == 1:
                print("   📦 Installation des dépendances...")
                dependances = analyse.get('dependances', [])
                
                # Nettoyer les dépendances pour Tkinter et autres packages GUI
                dependances_nettoyees = self._nettoyer_dependances_gui(dependances, analyse)
                
                # Ajouter automatiquement Bootstrap si interface web
                if analyse.get('besoin_interface', False) and analyse.get('type_interface') == 'web_gui':
                    if 'bootstrap' not in [d.lower() for d in dependances_nettoyees]:
                        dependances_nettoyees.append('Bootstrap via CDN (dans HTML)')
                
                self.gestionnaire_deps.installer_dependances(chemin_projet, dependances_nettoyees)
            
            print("   🔍 Validation de l'intégrité de l'application...")
            resultat_validation = self.validateur.valider_projet(chemin_projet)
            
            if not resultat_validation['succes']:
                print(f"   ⚠️  Problèmes détectés: {len(resultat_validation.get('erreurs', []))}")
                # Corriger automatiquement les problèmes détectés
                self._corriger_erreurs_validation(chemin_projet, resultat_validation)
            
            # TESTER L'APPLICATION COMPLÈTE
            print("   🧪 Test de l'application COMPLÈTE...")
            resultat_test = self.testeur.tester_application(chemin_projet)
            
            # GESTION AMÉLIORÉE POUR APPLICATIONS GUI
            app_type = resultat_test.get('type', 'console')
            
            if app_type == 'gui' and resultat_test.get('succes', False):
                print("  ✅ SUCCÈS | Application GUI prête (interface Tkinter)")
                succes = True
                
                self.apprentissage.enregistrer_reussite(
                    demande,
                    chemin_projet,
                    tentative
                )
                break
            elif resultat_test.get('succes', False):
                print("  SUCCÈS | Application COMPLÈTE fonctionnelle.")
                succes = True
                
                self.apprentissage.enregistrer_reussite(
                    demande,
                    chemin_projet,
                    tentative
                )
                break
            else:
                # Utiliser 'erreur' au lieu de 'error' (français vs anglais)
                erreur_msg = resultat_test.get('erreur', resultat_test.get('error', 'Erreur inconnue'))
                print(f"  X Échec: {erreur_msg}")
                
                # Détecter et corriger les bugs (si pas dernière tentative)
                if tentative < self.max_tentatives:
                    print("   🔧 Tentative de correction AUTO...")
                    bugs = self.detecteur.analyser_erreur(erreur_msg)
                    
                    # Correction intelligente basée sur l'analyse complète
                    correction = self.reparateur.corriger_erreur_complete(
                        chemin_projet,
                        bugs,
                        demande,
                        analyse
                    )
                    
                    if correction and correction.get('corrige'):
                        print(f"   ✨ Correction appliquée: {correction.get('action', 'Correction')}")
                        
                        # Apprendre de la correction
                        self.apprentissage.apprendre_erreur(
                            erreur_msg,
                            correction
                        )
        
        return succes, tentatives_effectuees
    
    def _nettoyer_dependances_gui(self, dependances, analyse):
        """Nettoie les dépendances pour les applications GUI"""
        dependances_nettoyees = []
        
        for dep in dependances:
            if isinstance(dep, str):
                dep_lower = dep.lower()
                
                # Gérer Tkinter (inclus avec Python)
                if 'tkinter' in dep_lower:
                    print(f"   → Tkinter: généralement inclus avec Python")
                    if sys.platform == "darwin":  # macOS
                        print(f"      ⚠️  Sur macOS, Tkinter peut nécessiter: brew install python-tk")
                    continue  # Ne pas installer via pip
                
                # Gérer SQLite (inclus avec Python)
                elif 'sqlite' in dep_lower:
                    print(f"   → SQLite: intégré à Python")
                    continue
                
                # Gérer les dépendances CDN
                elif 'cdn' in dep_lower or 'via cdn' in dep_lower:
                    print(f"   → {dep}: CDN - pas d'installation pip nécessaire")
                    continue
                
                # Normaliser matplotlib
                elif 'matplotlib' in dep_lower:
                    dependances_nettoyees.append('matplotlib')
                
                # Normaliser Flask-Bootstrap
                elif 'bootstrap' in dep_lower and 'flask' not in dep_lower:
                    dependances_nettoyees.append('Flask-Bootstrap')
                
                # Autres dépendances
                else:
                    dependances_nettoyees.append(dep)
        
        return dependances_nettoyees
    
    def _corriger_imports_flask(self, chemin_projet):
        """Corrige les imports Flask courants"""
        print("      🔍 Analyse des imports Python...")
        
        # Chercher tous les fichiers Python
        for root, dirs, files in os.walk(chemin_projet):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        original_content = content
                        modifications = []
                        
                        # Correction 1: flask_bootstrap → flask_bootstrap4
                        if 'from flask_bootstrap import Bootstrap' in content:
                            content = content.replace(
                                'from flask_bootstrap import Bootstrap',
                                'from flask_bootstrap4 import Bootstrap'
                            )
                            modifications.append("flask_bootstrap → flask_bootstrap4")
                        
                        # Correction 2: flask.ext.bootstrap (ancienne syntaxe)
                        if 'from flask.ext.bootstrap import Bootstrap' in content:
                            content = content.replace(
                                'from flask.ext.bootstrap import Bootstrap',
                                'from flask_bootstrap4 import Bootstrap'
                            )
                            modifications.append("flask.ext.bootstrap → flask_bootstrap4")
                        
                        # Correction 3: import flask_bootstrap (sans from)
                        if 'import flask_bootstrap' in content and 'flask_bootstrap4' not in content:
                            content = content.replace(
                                'import flask_bootstrap',
                                'import flask_bootstrap4'
                            )
                            modifications.append("import flask_bootstrap → flask_bootstrap4")
                        
                        # Si des modifications ont été faites, sauvegarder
                        if content != original_content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            print(f"      ✅ {file}: {', '.join(modifications)}")
                            
                    except UnicodeDecodeError:
                        # Essayer avec un autre encodage
                        try:
                            with open(file_path, 'r', encoding='latin-1') as f:
                                content = f.read()
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            print(f"      ✅ {file}: encodage corrigé (latin-1 → utf-8)")
                        except:
                            print(f"      ⚠️  {file}: erreur encodage, impossible de corriger")
                    except Exception as e:
                        print(f"      ⚠️  {file}: erreur correction: {e}")
    
    def _corriger_erreurs_validation(self, chemin_projet, resultat_validation):
        """Corrige automatiquement les erreurs de validation détectées"""
        if not resultat_validation.get('succes', True):
            print("   🔧 Application des corrections automatiques...")
            
            erreurs = resultat_validation.get('erreurs', [])
            
            for erreur in erreurs:
                if "API manquante" in erreur:
                    # Extraire l'URL manquante (ex: '/api/status')
                    import re
                    match = re.search(r"'([^']+)'", erreur)
                    if match:
                        url_manquante = match.group(1)
                        self._ajouter_route_api(chemin_projet, url_manquante)
                
                elif "Routes Flask manquantes" in erreur:
                    # Ajouter une route API de base
                    self._ajouter_route_api(chemin_projet, "/api/test")
        
        print("   ✅ Corrections de validation appliquées")
    
    def _ajouter_route_api(self, chemin_projet, url):
        """Ajoute une route API manquante au fichier main.py"""
        main_path = os.path.join(chemin_projet, "main.py")
        
        if not os.path.exists(main_path):
            print(f"      ⚠️  Fichier main.py non trouvé: {main_path}")
            return
        
        try:
            with open(main_path, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
            # Vérifier si la route existe déjà
            if f"@app.route('{url}')" in contenu or f'@app.route("{url}")' in contenu:
                print(f"      ✅ Route {url} existe déjà")
                return
            
            # Générer un nom de fonction à partir de l'URL
            nom_fonction = url.replace('/', '_').replace('-', '_').strip('_')
            if not nom_fonction:
                nom_fonction = 'api_endpoint'
            
            # Code de la nouvelle route
            nouvelle_route = f'''
# 🔧 ROUTE AJOUTÉE AUTOMATIQUEMENT (manquante dans le HTML)
@app.route('{url}')
def {nom_fonction}():
    import datetime
    return jsonify({{
        "status": "success",
        "endpoint": "{url}",
        "message": "Endpoint ajouté automatiquement",
        "timestamp": datetime.datetime.now().isoformat(),
        "data": {{"sample": "Données de démonstration"}}
    }})
'''
            
            # Insérer avant le if __name__ == "__main__":
            if 'if __name__ == "__main__":' in contenu:
                nouveau_contenu = contenu.replace(
                    'if __name__ == "__main__":',
                    f"{nouvelle_route}\n\nif __name__ == \"__main__\":"
                )
                
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write(nouveau_contenu)
                
                print(f"      ✅ Route ajoutée: {url}")
                
                # Mettre à jour aussi les appels dans le HTML
                self._corriger_appels_html(chemin_projet, url)
            else:
                print(f"      ⚠️  Impossible d'insérer la route {url}")
                
        except Exception as e:
            print(f"      ❌ Erreur ajout route {url}: {e}")
    
    def _corriger_appels_html(self, chemin_projet, url):
        """Corrige les appels API dans les templates HTML"""
        templates_dir = os.path.join(chemin_projet, "templates")
        
        if not os.path.exists(templates_dir):
            return
        
        for fichier in os.listdir(templates_dir):
            if fichier.endswith('.html'):
                html_path = os.path.join(templates_dir, fichier)
                try:
                    with open(html_path, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                    
                    # Chercher des appels fetch() problématiques
                    if 'fetch(' in contenu:
                        # Ajouter .catch() si manquant
                        lines = contenu.split('\n')
                        modifie = False
                        
                        for i, line in enumerate(lines):
                            if 'fetch(' in line and '.then(' in line and '.catch(' not in line:
                                lines[i] = line.rstrip(';') + '\\n        .catch(error => console.error("Erreur API:", error));'
                                modifie = True
                        
                        if modifie:
                            with open(html_path, 'w', encoding='utf-8') as f:
                                f.write('\\n'.join(lines))
                            print(f"      ✅ Gestion d'erreurs ajoutée dans {fichier}")
                            
                except Exception as e:
                    print(f"      ⚠️  Erreur correction HTML {fichier}: {e}")
    
    def _generer_rapport_final(self, chemin_projet, demande, tentatives, succes, analyse):
        """Génère un rapport final détaillé"""
        print("\n" + "=" * 60)
        print("📊 RAPPORT FINAL DÉTAILLÉ")
        print("=" * 60)
        print(f"📁 Projet: {os.path.basename(chemin_projet)}")
        print(f"📝 Demande: {demande[:80]}...")
        print(f"🔄 Tentatives: {tentatives}")
        print(f"🎯 Résultat: {'✅ RÉUSSI' if succes else '❌ ÉCHEC'}")
        
        print(f"\n🔍 ANALYSE TECHNIQUE:")
        print(f"   Type: {analyse.get('type_application', 'inconnu')}")
        print(f"   Interface: {'✅ Incluse' if analyse.get('besoin_interface', False) else '❌ Non nécessaire'}")
        
        if analyse.get('besoin_interface', False):
            print(f"   Type interface: {analyse.get('type_interface', 'inconnu')}")
            print(f"   Composants UI: {', '.join(analyse.get('composants_ui_attendus', []))}")
        
        print(f"   Fonctionnalités: {', '.join(analyse.get('fonctionnalites_cles', []))}")
        
        if succes:
            print(f"\n🎉 APPLICATION PRÊTE !")
            print(f"📁 Chemin: {chemin_projet}")
            
            # Instructions pour lancer l'application
            print(f"\n🚀 POUR LANCER L'APPLICATION:")
            print(f"   1. cd {chemin_projet}")
            
            # Chercher le fichier principal
            fichier_principal_trouve = False
            for f in os.listdir(chemin_projet):
                if f.endswith('.py') and f in ['main.py', 'app.py', 'run.py', 'application.py']:
                    print(f"   2. python {f}")
                    fichier_principal_trouve = True
                    
                    # Info supplémentaire selon le type d'interface
                    interface_type = analyse.get('type_interface', '')
                    if interface_type == 'web_gui':
                        print(f"   3. Ouvrir http://localhost:5000 dans votre navigateur")
                    elif interface_type == 'desktop_gui':
                        print(f"   3. L'application GUI Tkinter s'ouvrira automatiquement")
                    break
            
            if not fichier_principal_trouve:
                # Chercher n'importe quel fichier Python
                for f in os.listdir(chemin_projet):
                    if f.endswith('.py'):
                        print(f"   2. python {f}")
                        break
        
        print("=" * 60)
    
    def _generer_nom_projet(self, demande):
        """Crée un nom unique pour le projet"""
        import hashlib
        import re
        
        # Nettoyer la demande
        demande = demande.strip('"\'')
        
        timestamp = str(int(time.time()))[-6:]
        hash_demande = hashlib.md5(demande.encode()).hexdigest()[:6]
        
        # Prendre les 2 premiers mots significatifs
        mots = re.findall(r'\b\w+\b', demande.lower())[:2]
        base_nom = "_".join(mots) if len(mots) >= 2 else "application"
        
        # Nettoyer pour Windows
        base_nom = re.sub(r'[^\w\-]', '_', base_nom)
        base_nom = base_nom.strip('_')
        
        if not base_nom:
            base_nom = "app"
        
        return f"{base_nom}_{timestamp}_{hash_demande}"

def main():
    """Fonction principale"""
    print("=" * 70)
    print("🤖 ROBOT DÉVELOPPEUR - Générateur d'applications COMPLÈTES")
    print("=" * 70)
    print(f"⚙️  Modèle: {os.getenv('LLM_MODEL')}")
    print(f"🔄 Max tentatives: {os.getenv('MAX_TENTATIVES', 10)}")
    print(f"🌐 Frontend automatique: ✅ ACTIVÉ")
    print("-" * 70)
    
    robot = RobotDeveloppeur()
    
    # Mode interactif ou ligne de commande
    if len(sys.argv) > 1:
        demande = " ".join(sys.argv[1:])
        print(f"📨 Demande reçue: {demande}")
    else:
        print("💡 Exemples de demandes possibles:")
        print("   • 'application météo avec cartes et graphiques'")
        print("   • 'gestionnaire de contacts avec interface moderne'")
        print("   • 'jeu de memory avec cartes animées'")
        print("   • 'calculatrice scientifique avec interface web'")
        print("   • 'tableau de bord d'entreprise avec métriques'")
        print("-" * 70)
        demande = input("\n📝 Que veux-tu que je développe ?\n> ")
    
    if not demande.strip():
        print("❌ Aucune demande fournie.")
        return
    
    print(f"\n🎯 Lancement du développement pour: {demande}")
    print("⏳ Cela peut prendre quelques minutes...")
    
    resultat = robot.demarrer(demande)
    
    # Sauvegarder l'historique
    if resultat and resultat.get('succes'):
        with open("historique_reussites.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.ctime()}|{resultat['chemin']}|{demande[:50]}...\n")
    
    # Message final
    print("\n" + "=" * 70)
    if resultat.get('succes'):
        print("✨ DÉVELOPPEMENT TERMINÉ AVEC SUCCÈS !")
        print("🤖 Ton robot a généré une application COMPLÈTE et FONCTIONNELLE.")
    else:
        print("⚠️  Développement terminé avec des difficultés.")
        print("💡 Essayez de reformuler votre demande plus simplement.")
    print("=" * 70)

if __name__ == "__main__":
    main()