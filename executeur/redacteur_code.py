"""
✍️ Module de génération de code INTELLIGENT
Génère du code adapté backend + frontend automatiquement
"""

import os
import json
import time
import hashlib
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class CacheAPI:
    """Cache simple pour réduire les appels API"""
    def __init__(self, cache_dir="cache_api"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, demande, fichier_info, analyse):
        """Crée une clé de cache unique"""
        data = f"{demande}_{json.dumps(fichier_info, sort_keys=True)}_{json.dumps(analyse, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, key):
        """Récupère depuis le cache"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def set(self, key, data):
        """Sauvegarde dans le cache"""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

class RedacteurCode:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        self.cache = CacheAPI()  # INITIALISER LE CACHE ICI
    
    SYSTEM_PROMPT_CONCIS = """Tu es un expert en développement Python. Génère du code CONCIS et EFFICACE.
Utilise des noms de variables courts mais descriptifs.
Évite les commentaires excessifs.
Concentre-toi sur la fonctionnalité essentielle.

Pour les templates HTML, utilise du HTML minimal avec Bootstrap.
Pour Flask, utilise les routes minimales nécessaires.

Réponse avec UNIQUEMENT le code demandé, sans explications supplémentaires."""
    
    def generer_code(self, demande, fichier_info, analyse):
        """
        Ancienne méthode - gardée pour compatibilité
        """
        # Utilise la nouvelle méthode adaptative
        return self.generer_code_adapte(demande, fichier_info, analyse, "")
    
    def generer_code_adapte(self, demande, fichier_info, analyse, chemin_projet):
        """Génère du code adapté avec cache"""
        nom_fichier = fichier_info['nom']
        print(f"      📝 Génération adaptée pour: {nom_fichier}")
        
        # Créer clé de cache
        cache_key = self.cache.get_cache_key(demande, fichier_info, analyse)
        
        # Vérifier cache
        cached = self.cache.get(cache_key)
        if cached and cached.get('nom_fichier') == nom_fichier:
            print(f"      🔄 Code récupéré du cache: {nom_fichier}")
            return cached.get('code', '')
        
        # Sinon, générer via API
        try:
            code = self._generer_via_api(demande, fichier_info, analyse, chemin_projet)
            
            # Sauvegarder dans cache
            self.cache.set(cache_key, {
                'nom_fichier': nom_fichier,
                'code': code,
                'timestamp': time.time()
            })
            
            return code
            
        except Exception as e:
            print(f"❌ Erreur génération adaptée pour {nom_fichier}: {e}")
            # Utiliser du code de secours
            return self._code_de_secours(demande, nom_fichier, analyse)
    
    def _generer_via_api(self, demande, fichier_info, analyse, chemin_projet):
        """Génère du code via l'API Groq"""
        prompt = self._creer_prompt_intelligent(demande, fichier_info, analyse, chemin_projet)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT_CONCIS},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                timeout=30
            )
            
            code = response.choices[0].message.content
            code = self._nettoyer_code_genere(code, fichier_info['nom'])
            
            return code
            
        except Exception as e:
            raise Exception(f"Erreur API: {e}")
    
    def _creer_prompt_intelligent(self, demande, fichier_info, analyse, chemin_projet):
        """
        Crée un prompt intelligent adapté au type de fichier
        """
        nom_fichier = fichier_info["nom"]
        besoin_interface = analyse.get('besoin_interface', False)
        composants_ui = analyse.get('composants_ui_attendus', [])
        fonctionnalites = analyse.get('fonctionnalites_cles', [])
        
        prompt = f"""
        🎯 GÉNÉRATION DE CODE - FICHIER : {nom_fichier}
        
        📝 DEMANDE ORIGINALE :
        "{demande}"
        
        📊 ANALYSE TECHNIQUE COMPLÈTE :
        - Type d'application: {analyse.get('type_application')}
        - Besoin interface: {besoin_interface}
        - Type interface: {analyse.get('type_interface')}
        - Composants UI attendus: {composants_ui}
        - Fonctionnalités clés: {fonctionnalites}
        
        📁 CONTEXTE :
        - Fichier: {nom_fichier}
        - Description fichier: {fichier_info.get('description', 'Non spécifiée')}
        - Projet: {chemin_projet}
        """
        
        # Instructions spécifiques selon le type de fichier
        if nom_fichier.endswith('.py'):
            prompt += self._instructions_backend(demande, analyse, fonctionnalites)
        
        elif nom_fichier.endswith(('.html', '.htm')) or 'templates/' in nom_fichier:
            prompt += self._instructions_frontend_html(demande, analyse, composants_ui, fonctionnalites)
        
        elif nom_fichier.endswith('.css'):
            prompt += self._instructions_css(demande, analyse, composants_ui)
        
        elif nom_fichier.endswith('.js') or nom_fichier.endswith('.javascript'):
            prompt += self._instructions_javascript(demande, analyse, fonctionnalites)
        
        elif nom_fichier == "requirements.txt":
            prompt += self._instructions_requirements(analyse)
        
        else:
            prompt += self._instructions_generiques(demande, analyse)
        
        # Instructions générales
        prompt += """
        
        ⚡ INSTRUCTIONS GÉNÉRALES IMPORTANTES :
        1. Code COMPLET et IMMÉDIATEMENT FONCTIONNEL
        2. PAS de placeholders comme "[à compléter]", "[votre code ici]", "TODO"
        3. Toute la logique métier doit être implémentée
        4. Gestion des erreurs de base incluse
        5. Commentaires explicatifs en français
        6. Bonnes pratiques du langage respectées
        
        🎨 POUR LES INTERFACES :
        - Design MODERNE et RESPONSIVE (mobile-first)
        - Utiliser Bootstrap 5 + Font Awesome
        - UX intuitive et agréable
        
        📦 FORMAT DE RÉPONSE :
        Retourne UNIQUEMENT le code complet, sans texte supplémentaire.
        Pas de "Voici le code :", pas d'explications.
        """
        
        return prompt
    
    def _instructions_backend(self, demande, analyse, fonctionnalites):
        """Instructions pour les fichiers backend Python"""
        type_app = analyse.get('type_application', 'web')
        
        instructions = f"""
        
        🐍 BACKEND PYTHON - {type_app.upper()}
        
        IMPLÉMENTER TOUTES CES FONCTIONNALITÉS :
        {json.dumps(fonctionnalites, indent=2, ensure_ascii=False)}
        
        SPÉCIFICATIONS TECHNIQUES :
        1. Code Python complet et structuré
        2. """
        
        if type_app == 'web':
            instructions += """Utiliser Flask comme framework
        3. Toutes les routes nécessaires pour l'application
        4. Gestion des templates Jinja2
        5. Routes API si nécessaire (JSON responses)
        6. Gestion des erreurs HTTP
        7. Structure modulaire (fonctions séparées)
        """
        elif type_app == 'jeu':
            instructions += """Logique de jeu complète
        3. Gestion de l'état du jeu
        4. Système de score/niveaux
        5. Logique des règles
        6. Interface via Flask ou logique console
        """
        elif type_app == 'dashboard':
            instructions += """Génération de données pour le dashboard
        3. Calcul des statistiques/métriques
        4. API pour les données en temps réel
        5. Structure modulaire pour différentes visualisations
        """
        else:
            instructions += """Logique métier complète
        3. Fonctions bien structurées
        4. Gestion des entrées/sorties
        5. Code robuste avec validation
        """
        
        instructions += """
        8. Si données nécessaires → utiliser JSON file ou structure en mémoire
        9. Code prêt à être exécuté immédiatement
        10. 'if __name__ == "__main__":' avec lancement de l'app
        """
        
        return instructions
    
    def _instructions_frontend_html(self, demande, analyse, composants_ui, fonctionnalites):
        """Instructions pour les templates HTML"""
        instructions = f"""
        
        🌐 TEMPLATE HTML/JINJA2 - INTERFACE {analyse.get('type_interface').upper()}
        
        COMPOSANTS UI DEMANDÉS :
        {json.dumps(composants_ui, indent=2, ensure_ascii=False)}
        
        FONCTIONNALITÉS À SUPPORTER :
        {json.dumps(fonctionnalites, indent=2, ensure_ascii=False)}
        
        SPÉCIFICATIONS DU TEMPLATE :
        1. Template Jinja2 COMPLET pour Flask
        2. Utiliser Bootstrap 5 (CDN) pour le style
        3. Inclure Font Awesome (CDN) pour les icônes
        4. Design RESPONSIVE (mobile-first)
        5. Structure : doctype, html, head, body
        6. Header avec titre de l'application
        7. Main content avec tous les composants nécessaires
        8. JavaScript en bas du body pour performance
        """
        
        # Instructions spécifiques par composant
        if 'cartes' in composants_ui:
            instructions += """
        
        🃏 POUR LES CARTES :
        - Utiliser <div class="card"> de Bootstrap
        - Grille responsive avec row/col
        - Effets hover : card:hover { transform: translateY(-5px); }
        - Images/icons dans les cartes si pertinent
        - Boutons d'action dans chaque carte
        """
        
        if 'formulaires' in composants_ui:
            instructions += """
        
        📝 POUR LES FORMULAIRES :
        - Formulaires Bootstrap stylés
        - Validation HTML5 (required, pattern, etc.)
        - Labels clairs et placeholders
        - Boutons de soumission stylés
        - Messages d'erreur/succès
        """
        
        if 'tableaux' in composants_ui:
            instructions += """
        
        📊 POUR LES TABLEAUX :
        - Tableaux Bootstrap (table table-striped)
        - Responsive avec table-responsive
        - En-têtes clairs
        - Données dynamiques via Jinja2
        """
        
        if 'graphiques' in composants_ui:
            instructions += """
        
        📈 POUR LES GRAPHIQUES :
        - Conteneur pour Chart.js ou similar
        - Canvas HTML pour les graphiques
        - Légendes et axes clairs
        """
        
        if 'dashboard' in composants_ui:
            instructions += """
        
        🎛️ POUR LES DASHBOARDS :
        - Layout en grille avec sections
        - Cartes de métriques (KPI)
        - Graphiques et visualisations
        - Navigation entre vues
        """
        
        instructions += """
        
        9. CSS personnalisé dans <style> ou fichier séparé
        10. JavaScript pour l'interactivité
        11. Jinja2 syntax pour les données dynamiques
        """
        
        return instructions
    
    def _instructions_css(self, demande, analyse, composants_ui):
        """Instructions pour les fichiers CSS"""
        instructions = f"""
        
        🎨 CSS PERSONNALISÉ - COMPLÉMENT BOOTSTRAP
        
        COMPOSANTS À STYLISER :
        {json.dumps(composants_ui, indent=2, ensure_ascii=False)}
        
        SPÉCIFICATIONS CSS :
        1. CSS moderne (variables CSS, flexbox, grid)
        2. Complète Bootstrap, ne le remplace pas
        3. Design responsive (mobile-first)
        4. Variables CSS pour les couleurs/thème
        5. Animations subtiles pour l'interactivité
        6. Focus sur l'UX/UI
        7. Organisation logique (reset, variables, layout, components, utilities)
        """
        
        # Styles spécifiques par composant
        if 'cartes' in composants_ui:
            instructions += """
        
        /* Styles pour les cartes */
        .custom-card {
            transition: all 0.3s ease;
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .custom-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        }
        """
        
        if 'dashboard' in composants_ui:
            instructions += """
        
        /* Styles pour dashboard */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
        }
        """
        
        instructions += """
        
        8. Media queries pour le responsive
        9. Commentaires pour chaque section
        """
        
        return instructions
    
    def _instructions_javascript(self, demande, analyse, fonctionnalites):
        """Instructions pour les fichiers JavaScript"""
        instructions = f"""
        
        ⚡ JAVASCRIPT - INTERACTIVITÉ
        
        FONCTIONNALITÉS À IMPLÉMENTER :
        {json.dumps(fonctionnalites, indent=2, ensure_ascii=False)}
        
        SPÉCIFICATIONS JS :
        1. JavaScript moderne (ES6+)
        2. Code modulaire et organisé
        3. Gestion des événements utilisateur
        4. Communication avec backend (Fetch API)
        5. Validation des formulaires
        6. Mise à jour dynamique du DOM
        7. Gestion des erreurs (try/catch)
        """
        
        if 'graphiques' in analyse.get('composants_ui_attendus', []):
            instructions += """
        
        // Pour les graphiques (exemple avec Chart.js)
        const initCharts = () => {
            // Initialisation des graphiques
        };
        """
        
        instructions += """
        
        8. Documentation des fonctions
        9. Performant
        """
        
        return instructions
    
    def _instructions_requirements(self, analyse):
        """Instructions pour requirements.txt"""
        dependances = analyse.get('dependances', ['Flask'])
        
        instructions = f"""
        
        📦 REQUIREMENTS.TXT - DÉPENDANCES PYTHON
        
        DÉPENDANCES DÉTECTÉES :
        {json.dumps(dependances, indent=2, ensure_ascii=False)}
        
        FORMAT :
        Flask==2.3.3
        python-dotenv==1.0.0
        """
        
        return instructions
    
    def _instructions_generiques(self, demande, analyse):
        """Instructions pour les autres types de fichiers"""
        return f"""
        
        📄 FICHIER GÉNÉRIQUE
        
        CONTENU APPROPRIÉ pour ce type de fichier.
        Informations utiles pour le projet.
        Format approprié au type de fichier.
        """
    
    def _nettoyer_code_genere(self, code, nom_fichier):
        """Nettoie le code généré par l'API"""
        # Enlever les blocs de code markdown
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```html" in code:
            code = code.split("```html")[1].split("```")[0].strip()
        elif "```css" in code:
            code = code.split("```css")[1].split("```")[0].strip()
        elif "```javascript" in code:
            code = code.split("```javascript")[1].split("```")[0].strip()
        elif "```js" in code:
            code = code.split("```js")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        # Enlever les phrases d'introduction
        phrases_intro = [
            "Voici le code pour",
            "Here is the code for",
            "Code généré :",
            "Generated code:",
        ]
        
        for phrase in phrases_intro:
            if code.startswith(phrase):
                code = code[len(phrase):].strip()
        
        # Normaliser les sauts de ligne
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        
        # S'assurer qu'il y a un saut de ligne à la fin
        if code and not code.endswith('\n'):
            code += '\n'
        
        return code
    
    def _code_de_secours(self, demande, nom_fichier, analyse):
        """Code de secours si la génération échoue"""
        print(f"      ⚠️  Utilisation du code de secours pour {nom_fichier}")
        
        if nom_fichier.endswith(".py"):
            return f'''# {nom_fichier} - Généré par Robot Développeur
# Demande: {demande}
# Type d'application: {analyse.get('type_application', 'inconnu')}

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html', 
                         app_name="Application générée",
                         features={analyse.get('fonctionnalites_cles', [])})

@app.route('/api/data')
def api_data():
    """API de données"""
    return jsonify({{
        "status": "success",
        "message": "Application fonctionnelle",
        "features": {analyse.get('fonctionnalites_cles', [])}
    }})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''
        
        elif nom_fichier.endswith(('.html', '.htm')):
            return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application générée - {demande[:50]}</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        body {{
            background: #f8f9fa;
            padding: 20px;
        }}
        .app-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 30px;
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <h1><i class="fas fa-robot"></i> Application Générée</h1>
        <p>Demande: {demande}</p>
        
        <div class="alert alert-success">
            <h4>Fonctionnalités:</h4>
            <ul>
'''
            for feature in analyse.get('fonctionnalites_cles', ['Application fonctionnelle']):
                return_code += f'                <li>{feature}</li>\n'
            
            return_code += '''            </ul>
        </div>
        
        <div class="alert alert-info">
            Cette application a été générée automatiquement par le Robot Développeur
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
            return return_code
        
        elif nom_fichier.endswith('.css'):
            return '''/* CSS généré par Robot Développeur */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
}

.card {
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn {
    border-radius: 5px;
}
'''
        
        elif nom_fichier == "requirements.txt":
            deps = analyse.get('dependances', ['Flask'])
            deps_text = "\n".join([f"{dep}" for dep in deps])
            return f'''# Dépendances générées automatiquement
{deps_text}
python-dotenv
'''
        
        else:
            return f'''# Fichier {nom_fichier}
# Généré automatiquement
# Demande: {demande}
'''

# Test rapide
if __name__ == "__main__":
    print("🧪 Test du rédacteur de code amélioré...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    redacteur = RedacteurCode()
    
    # Test avec une analyse simulée
    analyse_test = {
        "type_application": "web",
        "besoin_interface": True,
        "type_interface": "web_gui",
        "composants_ui_attendus": ["cartes", "formulaires", "graphiques"],
        "fonctionnalites_cles": ["Ajouter des données", "Visualiser des graphiques", "Filtrer les résultats"],
        "description_technique": "Application de visualisation de données avec dashboard interactif",
        "dependances": ["Flask", "pandas", "matplotlib"]
    }
    
    fichier_info = {
        "nom": "app.py",
        "type": "code",
        "description": "Fichier principal Flask"
    }
    
    demande = "dashboard de données avec cartes de métriques et graphiques interactifs"
    
    print(f"\nTest pour: {demande}")
    code = redacteur.generer_code_adapte(demande, fichier_info, analyse_test, "/test/projet")
    
    print(f"\n📄 Code généré (premières 10 lignes):")
    print("=" * 60)
    for i, line in enumerate(code.split('\n')[:15]):
        print(f"{i+1:3}: {line}")
    print("=" * 60)