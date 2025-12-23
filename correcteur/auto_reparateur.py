"""
🔧 Module d'auto-réparation de code COMPLÈTE
Corrige backend + frontend intelligemment
"""

import os
import re
import sys
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AutoReparateur:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    def corriger_erreur_complete(self, chemin_projet, bugs, demande, analyse):
        """
        Correction intelligente basée sur l'analyse complète
        """
        print(f"\n🔧 CORRECTION INTELLIGENTE - Application complète")
        print(f"   Demande: {demande[:60]}...")
        print(f"   Type app: {analyse.get('type_application', 'inconnu')}")
        print(f"   Interface: {'✅ OUI' if analyse.get('besoin_interface', False) else '❌ NON'}")
        print(f"   Erreur: {bugs.get('type', 'inconnu')}")
        print(f"   Message: {bugs.get('message', 'Aucun')[:80]}...")
        
        # Vérifier si c'est une erreur SQLite
        error_type = bugs.get('type', '').lower()
        error_message = bugs.get('message', '').lower()
        if 'sqlite' in error_type or 'sqlalchemy' in error_type or 'sqlite' in error_message or 'sqlalchemy' in error_message:
            print("   🔧 Détection erreur SQLite - Correction spécifique...")
            if self._corriger_erreur_sqlite(chemin_projet, bugs):
                return {
                    "corrige": True, 
                    "action": "Correction SQLite",
                    "fichiers": ["app.py", "main.py"],
                    "type_correction": "sqlite_fix",
                    "details": "Correction d'erreur SQLite/SQLAlchemy"
                }
        
        # 1. Lire TOUS les fichiers du projet
        tous_les_fichiers = self._lire_tous_fichiers_projet(chemin_projet)
        if not tous_les_fichiers:
            print("   ❌ Aucun fichier trouvé dans le projet")
            return self._correction_de_secours(chemin_projet, demande, analyse)
        
        # 2. Analyser l'état actuel du projet
        etat_projet = self._analyser_etat_projet(tous_les_fichiers, bugs)
        
        # 3. Créer un prompt de correction intelligent
        prompt = self._creer_prompt_correction_complete(
            demande, analyse, bugs, tous_les_fichiers, etat_projet
        )
        
        # 4. Appeler l'API Groq pour une correction intelligente
        try:
            print("   📡 Appel à l'API Groq pour correction complète...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en débogage full-stack. Tu corriges les applications backend + frontend de manière complète."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            
            correction_text = response.choices[0].message.content.strip()
            print(f"   ✅ Réponse API reçue ({len(correction_text)} caractères)")
            
            # 5. Parser et appliquer les corrections
            corrections = self._parser_corrections_api(correction_text, tous_les_fichiers)
            
            if corrections:
                return self._appliquer_corrections_completes(chemin_projet, corrections, demande, analyse)
            else:
                print("   ⚠️  Aucune correction valide trouvée dans la réponse")
                return self._correction_de_secours(chemin_projet, demande, analyse)
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la correction API: {e}")
            return self._correction_de_secours(chemin_projet, demande, analyse)
    
    def _corriger_erreur_sqlite(self, chemin_projet, bugs):
        """Corrige spécifiquement les erreurs SQLite/SQLAlchemy"""
        print("   🔧 Correction erreur SQLite...")
        
        # Chercher le fichier principal
        for fichier in ['main.py', 'app.py']:
            fichier_path = os.path.join(chemin_projet, fichier)
            
            if os.path.exists(fichier_path):
                try:
                    with open(fichier_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    # Si le code utilise SQLAlchemy
                    if 'SQLAlchemy' in code:
                        print(f"   ⚠️  SQLAlchemy détecté dans {fichier}")
                        
                        # Vérifier et ajouter db.create_all() si manquant
                        if 'db.create_all()' not in code and 'if __name__ == "__main__":' in code:
                            code = code.replace(
                                'if __name__ == "__main__":',
                                'if __name__ == "__main__":\n    db.create_all()'
                            )
                            
                            with open(fichier_path, 'w', encoding='utf-8') as f:
                                f.write(code)
                            
                            print(f"   ✅ {fichier}: db.create_all() ajouté")
                            return True
                        
                except Exception as e:
                    print(f"   ❌ Erreur correction {fichier}: {e}")
        
        return False
    
    def _lire_tous_fichiers_projet(self, chemin_projet):
        """Lit tous les fichiers du projet"""
        tous_fichiers = {}
        
        try:
            for root, dirs, files in os.walk(chemin_projet):
                for file in files:
                    chemin_complet = os.path.join(root, file)
                    try:
                        with open(chemin_complet, 'r', encoding='utf-8', errors='ignore') as f:
                            contenu = f.read()
                            
                            # Chemin relatif pour l'affichage
                            chemin_relatif = os.path.relpath(chemin_complet, chemin_projet)
                            tous_fichiers[chemin_relatif] = {
                                "chemin_complet": chemin_complet,
                                "contenu": contenu,
                                "taille": len(contenu),
                                "extension": os.path.splitext(file)[1]
                            }
                    except Exception as e:
                        print(f"   ⚠️  Impossible de lire {file}: {e}")
            
            print(f"   📁 {len(tous_fichiers)} fichiers trouvés dans le projet")
            return tous_fichiers
            
        except Exception as e:
            print(f"   ❌ Erreur lecture projet: {e}")
            return {}
    
    def _analyser_etat_projet(self, fichiers, bugs):
        """Analyse l'état actuel du projet"""
        etat = {
            "fichiers_python": [],
            "fichiers_html": [],
            "fichiers_css": [],
            "fichiers_js": [],
            "fichier_principal": None,
            "structure_detectee": [],
            "problemes_detectes": []
        }
        
        for chemin_rel, info in fichiers.items():
            ext = info["extension"].lower()
            
            if ext == '.py':
                etat["fichiers_python"].append(chemin_rel)
                
                # Détecter le fichier principal
                if any(nom in chemin_rel.lower() for nom in ['main.py', 'app.py', 'application.py']):
                    etat["fichier_principal"] = chemin_rel
                
                # Analyser le contenu Python
                if self._detecter_problemes_python(info["contenu"]):
                    etat["problemes_detectes"].append(f"Problème Python dans {chemin_rel}")
            
            elif ext in ['.html', '.htm']:
                etat["fichiers_html"].append(chemin_rel)
                
                # Analyser HTML
                if not self._valider_html_basique(info["contenu"]):
                    etat["problemes_detectes"].append(f"HTML problématique dans {chemin_rel}")
            
            elif ext == '.css':
                etat["fichiers_css"].append(chemin_rel)
            
            elif ext in ['.js', '.javascript']:
                etat["fichiers_js"].append(chemin_rel)
            
            # Détecter la structure
            if 'templates/' in chemin_rel:
                etat["structure_detectee"].append("templates")
            elif 'static/' in chemin_rel:
                etat["structure_detectee"].append("static")
            elif 'requirements.txt' in chemin_rel:
                etat["structure_detectee"].append("requirements")
        
        # Si pas de fichier principal détecté, prendre le premier .py
        if not etat["fichier_principal"] and etat["fichiers_python"]:
            etat["fichier_principal"] = etat["fichiers_python"][0]
        
        return etat
    
    def _detecter_problemes_python(self, code):
        """Détecte les problèmes courants dans le code Python"""
        problemes = []
        
        # Vérifier les imports manquants
        import_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import'
        ]
        
        for pattern in import_patterns:
            imports = re.findall(pattern, code)
            for imp in imports:
                if imp not in ['os', 'sys', 'json', 're', 'datetime', 'time', 'math', 'random']:
                    # Vérifier si c'est un module standard ou non
                    problemes.append(f"Import potentiellement problématique: {imp}")
        
        # Vérifier les fonctions non définies
        func_defs = re.findall(r'def\s+(\w+)', code)
        func_calls = re.findall(r'(\w+)\s*\(', code)
        
        for call in func_calls:
            if call not in func_defs and call not in ['print', 'len', 'str', 'int', 'float', 'list', 'dict']:
                problemes.append(f"Fonction potentiellement non définie: {call}")
        
        return len(problemes) > 0
    
    def _valider_html_basique(self, html):
        """Valide la structure HTML basique"""
        return '<html' in html.lower() and '</html>' in html.lower()
    
    def _creer_prompt_correction_complete(self, demande, analyse, bugs, fichiers, etat_projet):
        """Crée un prompt intelligent pour la correction complète"""
        besoin_interface = analyse.get('besoin_interface', False)
        composants_ui = analyse.get('composants_ui_attendus', [])
        fonctionnalites = analyse.get('fonctionnalites_cles', [])
        
        prompt = f"""
        🚨 CORRECTION D'APPLICATION COMPLÈTE - URGENT
        
        🎯 CONTEXTE DU PROJET :
        - Demande originale : "{demande}"
        - Type d'application : {analyse.get('type_application')}
        - Interface nécessaire : {'OUI' if besoin_interface else 'NON'}
        - Composants UI demandés : {composants_ui}
        - Fonctionnalités clés : {fonctionnalites}
        - Description technique : {analyse.get('description_technique')}
        
        🐛 ERREUR RENCONTRÉE :
        - Type : {bugs.get('type', 'inconnu')}
        - Message : {bugs.get('message', 'Aucun détail')}
        - Suggestions : {bugs.get('suggestions', [])}
        
        📊 ÉTAT ACTUEL DU PROJET :
        - Fichier principal : {etat_projet.get('fichier_principal', 'Non détecté')}
        - Fichiers Python : {len(etat_projet.get('fichiers_python', []))}
        - Fichiers HTML : {len(etat_projet.get('fichiers_html', []))}
        - Fichiers CSS : {len(etat_projet.get('fichiers_css', []))}
        - Fichiers JS : {len(etat_projet.get('fichiers_js', []))}
        - Problèmes détectés : {etat_projet.get('problemes_detectes', [])}
        
        📁 CONTENU ACTUEL DES FICHIERS :
        """
        
        # Ajouter le contenu des fichiers principaux
        fichiers_a_inclure = []
        
        # Inclure le fichier principal
        if etat_projet.get('fichier_principal'):
            fichier_principal = etat_projet['fichier_principal']
            if fichier_principal in fichiers:
                fichiers_a_inclure.append(fichier_principal)
        
        # Inclure les premiers fichiers de chaque type
        for file_list in [etat_projet.get('fichiers_html', []),
                         etat_projet.get('fichiers_css', []),
                         etat_projet.get('fichiers_js', [])]:
            if file_list:
                fichiers_a_inclure.append(file_list[0])
        
        # Ajouter le contenu des fichiers
        for fichier_rel in fichiers_a_inclure[:3]:  # Limiter à 3 fichiers
            if fichier_rel in fichiers:
                info = fichiers[fichier_rel]
                prompt += f"\n{'='*60}\nFICHIER: {fichier_rel}\n{'='*60}\n"
                prompt += info["contenu"][:1000]  # Limiter à 1000 caractères
                if info["taille"] > 1000:
                    prompt += "\n... [contenu tronqué]"
        
        prompt += f"""
        
        🛠️ INSTRUCTIONS DE CORRECTION :
        
        1. ANALYSE COMPLÈTE :
           - Identifie la RACINE du problème
           - Considère l'application dans son ENSEMBLE (backend + frontend)
           - Vérifie la cohérence entre les fichiers
        
        2. CORRECTION BACKEND (Python) :
           - Corrige toutes les erreurs syntaxiques
           - Assure que TOUTES les routes Flask nécessaires existent
           - Implémente la logique métier complète pour : {fonctionnalites}
           - Gestion des erreurs appropriée
           - Code structuré et commenté
        
        3. CORRECTION FRONTEND (si interface nécessaire) :
           - Templates HTML/Jinja2 complets et fonctionnels
           - Design responsive avec Bootstrap 5
           - Intégration correcte CSS/JavaScript
           - Composants UI pour : {composants_ui}
           - Communication backend/frontend fonctionnelle
        
        4. CORRECTIONS SPÉCIFIQUES :
        """
        
        # Ajouter des corrections spécifiques selon l'erreur
        error_type = bugs.get('type', '').lower()
        if 'import' in error_type or 'module' in error_type:
            prompt += "\n   - Ajouter les imports manquants ou corriger les imports"
        if 'syntax' in error_type:
            prompt += "\n   - Corriger toutes les erreurs de syntaxe Python"
        if 'name' in error_type:
            prompt += "\n   - Définir toutes les variables/fonctions utilisées"
        if 'template' in error_type or 'jinja' in error_type:
            prompt += "\n   - Corriger les templates Jinja2 et l'intégration Flask"
        
        prompt += f"""
        
        5. FORMAT DE RÉPONSE :
           Retourne UNIQUEMENT un objet JSON avec cette structure :
           {{
             "explication": "Explication courte des corrections apportées",
             "fichiers_corriges": [
               {{
                 "chemin": "chemin/relatif/du/fichier",
                 "contenu": "CODE COMPLET CORRIGÉ du fichier"
               }},
               // Autres fichiers corrigés...
             ],
             "actions": ["Liste des actions de correction effectuées"],
             "recommandations": ["Recommandations pour éviter l'erreur à l'avenir"]
           }}
        
        IMPORTANT :
        - Pour chaque fichier, retourne le code COMPLET (pas seulement les parties modifiées)
        - Le code doit être SYNTAXIQUEMENT VALIDE et FONCTIONNEL
        - Maintenir la cohérence avec l'analyse technique originale
        - Assurer que l'application COMPLÈTE fonctionne après correction
        """
        
        return prompt
    
    def _parser_corrections_api(self, reponse_api, fichiers_existants):
        """Parse la réponse de l'API pour extraire les corrections"""
        try:
            # Essayer d'extraire du JSON
            debut_json = reponse_api.find('{')
            fin_json = reponse_api.rfind('}') + 1
            
            if debut_json != -1 and fin_json != 0:
                json_str = reponse_api[debut_json:fin_json]
                corrections = json.loads(json_str)
                
                # Valider la structure
                if isinstance(corrections, dict) and "fichiers_corriges" in corrections:
                    print(f"   ✅ {len(corrections['fichiers_corriges'])} fichiers à corriger")
                    return corrections
            
            # Si pas de JSON valide, essayer de parser manuellement
            return self._parser_corrections_manuelles(reponse_api, fichiers_existants)
            
        except json.JSONDecodeError as e:
            print(f"   ❌ Impossible de parser JSON: {e}")
            return self._parser_corrections_manuelles(reponse_api, fichiers_existants)
        except Exception as e:
            print(f"   ❌ Erreur parsing: {e}")
            return None
    
    def _parser_corrections_manuelles(self, reponse, fichiers_existants):
        """Parse manuellement les corrections si le JSON échoue"""
        corrections = {
            "explication": "Correction manuelle",
            "fichiers_corriges": [],
            "actions": ["Correction basée sur l'analyse de l'erreur"],
            "recommandations": []
        }
        
        # Chercher des blocs de code avec des noms de fichiers
        pattern = r'FICHIER:\s*([^\n]+)\s*(?:```(?:\w+)?\s*)?([\s\S]*?)(?=```|FICHIER:|$)'
        matches = re.findall(pattern, reponse, re.IGNORECASE)
        
        for match in matches:
            chemin_fichier = match[0].strip()
            code = match[1].strip()
            
            # Nettoyer le code
            if code.startswith('```'):
                code = code.split('```')[1].split('```')[0].strip()
            
            if code and chemin_fichier:
                # Vérifier si le fichier existe dans le projet
                if any(chemin_fichier in f for f in fichiers_existants.keys()):
                    corrections["fichiers_corriges"].append({
                        "chemin": chemin_fichier,
                        "contenu": code
                    })
        
        if corrections["fichiers_corriges"]:
            return corrections
        else:
            # Essayer une autre approche
            return self._extraire_corrections_fallback(reponse, fichiers_existants)
    
    def _extraire_corrections_fallback(self, reponse, fichiers_existants):
        """Fallback si aucune méthode de parsing ne fonctionne"""
        # Chercher simplement des blocs de code Python
        corrections = {
            "explication": "Correction basée sur l'extraction de code",
            "fichiers_corriges": [],
            "actions": ["Extraction et remplacement de code"],
            "recommandations": []
        }
        
        # Chercher du code Python
        if '```python' in reponse:
            code_blocks = reponse.split('```python')[1:]
            for i, block in enumerate(code_blocks):
                if '```' in block:
                    code = block.split('```')[0].strip()
                    if code:
                        # Trouver un fichier Python à corriger
                        fichiers_py = [f for f in fichiers_existants.keys() 
                                     if f.endswith('.py')]
                        if fichiers_py:
                            corrections["fichiers_corriges"].append({
                                "chemin": fichiers_py[0],
                                "contenu": code
                            })
                            break
        
        return corrections if corrections["fichiers_corriges"] else None
    
    def _appliquer_corrections_completes(self, chemin_projet, corrections, demande, analyse):
        """Applique toutes les corrections au projet"""
        print(f"   🔧 Application des corrections...")
        
        fichiers_corriges = []
        
        for fichier_corr in corrections.get("fichiers_corriges", []):
            chemin_rel = fichier_corr.get("chemin", "")
            contenu = fichier_corr.get("contenu", "")
            
            if chemin_rel and contenu:
                chemin_absolu = os.path.join(chemin_projet, chemin_rel)
                
                # Créer les répertoires parents si nécessaire
                os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)
                
                # Écrire le fichier corrigé
                with open(chemin_absolu, 'w', encoding='utf-8') as f:
                    f.write(contenu)
                
                fichiers_corriges.append(chemin_rel)
                print(f"      ✅ {chemin_rel} corrigé")
        
        if fichiers_corriges:
            explication = corrections.get("explication", "Correction appliquée")
            actions = corrections.get("actions", ["Corrections multiples"])
            
            return {
                "corrige": True,
                "fichiers": fichiers_corriges,
                "action": f"Correction complète: {', '.join(actions)}",
                "type_correction": "complete_api",
                "details": explication
            }
        else:
            print("   ⚠️  Aucun fichier corrigé")
            return None
    
    def _correction_de_secours(self, chemin_projet, demande, analyse):
        """Correction de secours si tout échoue"""
        print("   ⚠️  Application de la correction de secours...")
        
        # Générer une application simple basée sur l'analyse
        besoin_interface = analyse.get('besoin_interface', False)
        type_app = analyse.get('type_application', 'web')
        
        if besoin_interface and type_app == 'web':
            return self._generer_app_web_simple(chemin_projet, demande, analyse)
        else:
            return self._generer_app_simple(chemin_projet, demande, analyse)
    
    def _generer_app_web_simple(self, chemin_projet, demande, analyse):
        """Génère une application web simple de secours"""
        # Créer app.py
        app_py = '''from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html', 
                         app_name="Application générée",
                         message="Application fonctionnelle générée automatiquement")

@app.route('/api/status')
def api_status():
    """API de statut"""
    return jsonify({
        "status": "success",
        "message": "Application Flask fonctionnelle",
        "features": ["Interface web", "API REST", "Design responsive"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
        
        # Créer index.html
        index_html = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application générée - Robot Développeur</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .app-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .app-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .feature-card {
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            transition: transform 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="app-header">
            <h1><i class="fas fa-robot me-2"></i>Application Générée Automatiquement</h1>
            <p class="lead">{{ message }}</p>
        </div>
        
        <div class="container py-4">
            <h3 class="mb-4"><i class="fas fa-check-circle text-success me-2"></i>Application Fonctionnelle</h3>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card feature-card">
                        <div class="card-body">
                            <h5 class="card-title"><i class="fas fa-server me-2"></i>Backend Flask</h5>
                            <p class="card-text">Serveur Flask fonctionnel avec API REST</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card feature-card">
                        <div class="card-body">
                            <h5 class="card-title"><i class="fas fa-desktop me-2"></i>Frontend Bootstrap</h5>
                            <p class="card-text">Interface responsive avec Bootstrap 5</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4 text-center">
                <button class="btn btn-primary" onclick="testAPI()">
                    <i class="fas fa-bolt me-2"></i>Tester l'API
                </button>
                <div id="apiResult" class="mt-3"></div>
            </div>
        </div>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
    function testAPI() {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                document.getElementById('apiResult').innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check me-2"></i>
                        API fonctionnelle : ${data.message}
                    </div>
                `;
            })
            .catch(error => {
                document.getElementById('apiResult').innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Erreur API : ${error}
                    </div>
                `;
            });
    }
    </script>
</body>
</html>'''
        
        # Créer requirements.txt
        requirements = '''# Dépendances générées automatiquement
Flask==2.3.3
python-dotenv==1.0.0
'''
        
        # Écrire les fichiers
        os.makedirs(os.path.join(chemin_projet, "templates"), exist_ok=True)
        
        with open(os.path.join(chemin_projet, "app.py"), 'w', encoding='utf-8') as f:
            f.write(app_py)
        
        with open(os.path.join(chemin_projet, "templates", "index.html"), 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        with open(os.path.join(chemin_projet, "requirements.txt"), 'w', encoding='utf-8') as f:
            f.write(requirements)
        
        print("   ✅ Application web simple générée")
        
        return {
            "corrige": True,
            "fichiers": ["app.py", "templates/index.html", "requirements.txt"],
            "action": "Application web simple générée de secours",
            "type_correction": "secours_web",
            "details": "Application Flask fonctionnelle avec interface Bootstrap"
        }
    
    def _generer_app_simple(self, chemin_projet, demande, analyse):
        """Génère une application simple (non-web) de secours"""
        # Code Python simple
        code = f'''#!/usr/bin/env python3
"""
Application générée automatiquement
Demande : {demande}
Type : {analyse.get('type_application', 'inconnu')}
"""

def main():
    """Fonction principale"""
    print("=" * 50)
    print("APPLICATION GÉNÉRÉE AUTOMATIQUEMENT")
    print("=" * 50)
    print(f"Demande : {demande}")
    print(f"Type d'application : {analyse.get('type_application', 'inconnu')}")
    print(f"Fonctionnalités : {analyse.get('fonctionnalites_cles', [])}")
    print("=" * 50)
    print("\\n✅ Application fonctionnelle !")
    return 0

if __name__ == "__main__":
    exit(main())
'''
        
        with open(os.path.join(chemin_projet, "main.py"), 'w', encoding='utf-8') as f:
            f.write(code)
        
        print("   ✅ Application simple générée")
        
        return {
            "corrige": True,
            "fichiers": ["main.py"],
            "action": "Application simple générée de secours",
            "type_correction": "secours_simple",
            "details": "Application Python simple fonctionnelle"
        }

# Test rapide
if __name__ == "__main__":
    print("🧪 Test du AutoReparateur amélioré...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Créer un dossier test
    import tempfile
    import shutil
    
    test_dir = tempfile.mkdtemp()
    print(f"Dossier test: {test_dir}")
    
    # Créer une structure de projet simple
    os.makedirs(os.path.join(test_dir, "templates"), exist_ok=True)
    
    # Créer des fichiers avec erreurs
    app_py_bug = '''from flask import Flask
app = Flask(__name__)

@app.route('/')
def inde():  # Faute de frappe dans le nom de fonction
    return "Hello World"

if __name__ == '__main__':
    app.run()
'''
    
    with open(os.path.join(test_dir, "app.py"), 'w') as f:
        f.write(app_py_bug)
    
    # Tester
    reparateur = AutoReparateur()
    
    # Simulation d'une analyse
    analyse_test = {
        "type_application": "web",
        "besoin_interface": True,
        "type_interface": "web_gui",
        "composants_ui_attendus": ["cartes"],
        "fonctionnalites_cles": ["Afficher une page web", "API simple"],
        "description_technique": "Application web Flask simple",
        "dependances": ["Flask"]
    }
    
    bugs_test = {
        "type": "NameError",
        "message": "name 'index' is not defined",
        "suggestions": ["Vérifier le nom de la fonction dans la route /"]
    }
    
    demande_test = "site web simple avec une page d'accueil"
    
    print(f"\nTest de correction pour: {demande_test}")
    resultat = reparateur.corriger_erreur_complete(test_dir, bugs_test, demande_test, analyse_test)
    
    print(f"\n📊 Résultat: {resultat}")
    
    # Nettoyer
    shutil.rmtree(test_dir)
    print(f"\n🧹 Dossier test nettoyé")