"""
 Module de conception d'architecture MULTI-LANGAGE
Détermine la structure de fichiers pour un projet dans n'importe quel langage
"""

import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class Architecte:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    
    def creer_architecture(self, analyse):
        """
        Crée une architecture de projet basée sur l'analyse AVEC LANGAGE
        """
        
        langage = analyse.get('langage_principal', 'python')
        type_app = analyse.get('type_application', 'web')
        besoin_interface = analyse.get('besoin_interface', False)
        framework_ui = analyse.get('framework_ui', '')
        
        print(f"     Architecture pour: {langage.upper()} - {type_app}")
        
        
        architecture_base = self._architecture_par_langage(langage, type_app, besoin_interface, framework_ui, analyse)
        
       
        try:
            prompt = self._creer_prompt_architecture(analyse, langage, type_app)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Tu es un architecte logiciel expert en {langage}. Retourne uniquement du JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            content = self._nettoyer_json(content)
            
            api_architecture = json.loads(content)
            
            
            architecture = self._fusionner_architectures(architecture_base, api_architecture)
            
        except Exception as e:
            print(f"    Erreur API architecture: {e}")
            architecture = architecture_base
        
        
        architecture = self._filtrer_architecture(architecture)
        
        print(f"   {len(architecture.get('fichiers', []))} fichiers, {len(architecture.get('structure_dossiers', []))} dossiers")
        
        return architecture
    
    def _architecture_par_langage(self, langage, type_app, besoin_interface, framework_ui, analyse):
        """Retourne l'architecture adaptée au langage"""
        # Architecture par défaut minimale
        architecture = {
            "nom_projet": self._generer_nom_projet(analyse, langage),
            "fichiers": [],
            "structure_dossiers": [],
            "point_entree": ""
        }
        
        # Ajouter des fichiers communs selon le langage
        if langage == 'go':
            architecture['fichiers'].extend([
                {"nom": "main.go", "type": "code", "description": "Point d'entrée principal Go"},
                {"nom": "go.mod", "type": "config", "description": "Module Go avec dépendances"},
                {"nom": "README.md", "type": "documentation", "description": "Documentation du projet"},
                {"nom": ".gitignore", "type": "config", "description": "Fichiers à ignorer pour Go"}
            ])
            architecture['structure_dossiers'] = ["cmd/", "internal/", "pkg/", "config/"]
            architecture['point_entree'] = "main.go"
            
            if type_app in ['web', 'api']:
                architecture['fichiers'].extend([
                    {"nom": "cmd/api/main.go", "type": "code", "description": "Serveur HTTP API"},
                    {"nom": "internal/handlers/handlers.go", "type": "code", "description": "Handlers HTTP"},
                    {"nom": "internal/models/models.go", "type": "code", "description": "Structs et modèles Go"}
                ])
            
        elif langage == 'javascript':
            architecture['fichiers'].extend([
                {"nom": "package.json", "type": "config", "description": "Dépendances NPM"},
                {"nom": "README.md", "type": "documentation", "description": "Documentation"},
                {"nom": ".gitignore", "type": "config", "description": "Fichiers à ignorer pour Node"}
            ])
            architecture['point_entree'] = "index.html" if besoin_interface else "server.js"
            
            if besoin_interface:
                if framework_ui == 'react':
                    architecture['fichiers'].extend([
                        {"nom": "src/App.jsx", "type": "code", "description": "Composant principal React"},
                        {"nom": "src/index.js", "type": "code", "description": "Point d'entrée React"},
                        {"nom": "public/index.html", "type": "template", "description": "Template HTML"}
                    ])
                    architecture['structure_dossiers'] = ["src/", "public/", "components/", "hooks/"]
                else:
                    architecture['fichiers'].extend([
                        {"nom": "index.html", "type": "template", "description": "Page principale"},
                        {"nom": "src/main.js", "type": "code", "description": "Logique JavaScript principale"}
                    ])
                    architecture['structure_dossiers'] = ["src/", "public/"]
            
            if type_app in ['web', 'api'] and not (besoin_interface and framework_ui == 'react'):
                architecture['fichiers'].extend([
                    {"nom": "server.js", "type": "code", "description": "Serveur Express.js"}
                ])
                architecture['structure_dossiers'].append("routes/")
                
        elif langage == 'typescript':
            architecture['fichiers'].extend([
                {"nom": "package.json", "type": "config", "description": "Dépendances NPM"},
                {"nom": "README.md", "type": "documentation", "description": "Documentation"},
                {"nom": "tsconfig.json", "type": "config", "description": "Configuration TypeScript"},
                {"nom": ".gitignore", "type": "config", "description": "Fichiers à ignorer"}
            ])
            architecture['point_entree'] = "src/index.ts"
            architecture['structure_dossiers'] = ["src/", "dist/", "types/"]
            
            if besoin_interface and framework_ui == 'react':
                architecture['fichiers'].extend([
                    {"nom": "src/App.tsx", "type": "code", "description": "Composant principal React TypeScript"},
                    {"nom": "src/index.tsx", "type": "code", "description": "Point d'entrée React"}
                ])
                
        elif langage == 'rust':
            architecture['fichiers'].extend([
                {"nom": "Cargo.toml", "type": "config", "description": "Configuration Cargo"},
                {"nom": "README.md", "type": "documentation", "description": "Documentation"},
                {"nom": ".gitignore", "type": "config", "description": "Fichiers à ignorer pour Rust"},
                {"nom": "src/main.rs", "type": "code", "description": "Point d'entrée Rust"}
            ])
            architecture['structure_dossiers'] = ["src/", "tests/", "examples/"]
            architecture['point_entree'] = "src/main.rs"
            
            if type_app in ['web', 'api']:
                architecture['fichiers'].extend([
                    {"nom": "src/lib.rs", "type": "code", "description": "Bibliothèque principale"},
                    {"nom": "src/handlers/mod.rs", "type": "code", "description": "Handlers HTTP"}
                ])
                
        elif langage == 'python':
            architecture['fichiers'].extend([
                {"nom": "main.py", "type": "code", "description": "Point d'entrée principal"},
                {"nom": "requirements.txt", "type": "config", "description": "Dépendances Python"},
                {"nom": "README.md", "type": "documentation", "description": "Documentation du projet"},
                {"nom": ".gitignore", "type": "config", "description": "Fichiers à ignorer pour Python"}
            ])
            architecture['point_entree'] = "main.py"
            
            if framework_ui == 'streamlit':
                architecture['fichiers'].append({"nom": "app.py", "type": "code", "description": "Application Streamlit"})
                architecture['structure_dossiers'] = ["pages/", "data/", "utils/"]
            elif framework_ui == 'flask_html':
                architecture['fichiers'].extend([
                    {"nom": "app.py", "type": "code", "description": "Application Flask principale"},
                    {"nom": "models.py", "type": "code", "description": "Modèles de données"}
                ])
                architecture['structure_dossiers'] = ["templates/", "static/", "instance/"]
                
                if besoin_interface:
                    architecture['fichiers'].extend([
                        {"nom": "templates/index.html", "type": "template", "description": "Template HTML principal"},
                        {"nom": "static/style.css", "type": "style", "description": "Feuille de style CSS"}
                    ])
                    
        else:
           
            extension = self._get_extension_langage(langage)
            architecture['fichiers'].extend([
                {"nom": f"main.{extension}", "type": "code", "description": f"Point d'entrée {langage}"},
                {"nom": "README.md", "type": "documentation", "description": "Documentation du projet"},
                {"nom": ".gitignore", "type": "config", "description": f"Fichiers à ignorer pour {langage}"}
            ])
            architecture['structure_dossiers'] = ["src/", "lib/", "docs/"]
            architecture['point_entree'] = f"main.{extension}"
        
        
        architecture['fichiers'].append({"nom": ".env.example", "type": "config", "description": "Variables d'environnement"})
        
        if any(mot in analyse.get('description_technique', '').lower() for mot in ['docker', 'container', 'image']):
            architecture['fichiers'].append({"nom": "Dockerfile", "type": "config", "description": "Conteneurisation Docker"})
        
        return architecture
    
    def _creer_prompt_architecture(self, analyse, langage, type_app):
        """Crée un prompt pour l'API d'architecture"""
        return f"""
        À partir de cette analyse de projet, crée une architecture de fichiers COMPLÈTE.
        Retourne UNIQUEMENT un JSON valide.
        
        ANALYSE : {json.dumps(analyse, indent=2)}
        
        IMPORTANT : 
        - Langage principal: {langage}
        - Type d'application: {type_app}
        - Ne pas inclure de dossiers dans la liste 'fichiers' - uniquement des fichiers.
        - Les dossiers doivent aller dans 'structure_dossiers'.
        
        Retourne un JSON avec ces champs EXACTS :
        - nom_projet : nom suggéré (sans caractères spéciaux, underscore pour espaces)
        - fichiers : liste d'objets avec 'nom', 'type', 'description' (UNIQUEMENT DES FICHIERS, PAS DE DOSSIERS)
        - structure_dossiers : liste de dossiers à créer (terminés par /)
        - point_entree : nom du fichier principal (ex: main.py, main.go, index.js)
        
        EXEMPLES POUR {langage.upper()} :
        """
    
    def _generer_nom_projet(self, analyse, langage):
        """Génère un nom de projet basé sur l'analyse"""
        type_app = analyse.get('type_application', 'app')
        description = analyse.get('description_technique', 'projet')
        
        
        mots = description.lower().split()[:3]
        nom_mots = "_".join(mots[:2]) if len(mots) >= 2 else type_app
        
        
        nom = f"{nom_mots}_{langage}_project"
        nom = nom.replace('-', '_').replace(' ', '_').replace('.', '_').lower()
        
        return nom
    
    def _get_extension_langage(self, langage):
        """Retourne l'extension de fichier pour un langage"""
        extensions = {
            'go': 'go',
            'javascript': 'js',
            'typescript': 'ts',
            'rust': 'rs',
            'python': 'py',
            'java': 'java',
            'c++': 'cpp',
            'c': 'c',
            'php': 'php',
            'ruby': 'rb',
            'bash': 'sh',
            'html': 'html',
            'css': 'css',
            'sql': 'sql',
            'yaml': 'yaml',
            'json': 'json',
            'markdown': 'md'
        }
        return extensions.get(langage, 'txt')
    
    def _fusionner_architectures(self, architecture_base, architecture_api):
        """Fusionne l'architecture de base avec celle de l'API"""
        fusion = architecture_base.copy()
        
        
        fichiers_fusion = {f['nom']: f for f in architecture_base.get('fichiers', [])}
        
        for fichier in architecture_api.get('fichiers', []):
            if isinstance(fichier, dict) and 'nom' in fichier:
                fichiers_fusion[fichier['nom']] = fichier
        
        fusion['fichiers'] = list(fichiers_fusion.values())
        
        
        dossiers_fusion = set(architecture_base.get('structure_dossiers', []))
        dossiers_fusion.update(architecture_api.get('structure_dossiers', []))
        
        fusion['structure_dossiers'] = list(dossiers_fusion)
        
        
        if 'point_entree' in architecture_api and architecture_api['point_entree']:
            fusion['point_entree'] = architecture_api['point_entree']
        
        return fusion
    
    def _nettoyer_json(self, content):
        """Nettoie le JSON retourné par l'API"""
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        
        lines = content.split('\n')
        json_lines = []
        
        for line in lines:
            if line.strip().startswith('//') or line.strip().startswith('#'):
                continue
            if line.strip() == '':
                continue
            json_lines.append(line)
        
        return '\n'.join(json_lines)
    
    def _filtrer_architecture(self, architecture):
        """Filtre l'architecture pour enlever les dossiers de la liste fichiers"""
        if 'fichiers' not in architecture:
            architecture['fichiers'] = []
        
       
        fichiers_filtres = []
        for fichier in architecture.get('fichiers', []):
            if isinstance(fichier, dict) and 'nom' in fichier:
                nom = fichier['nom']
                
                if not nom.endswith('/') and '/' not in nom.split('/')[-1:]:
                    fichiers_filtres.append(fichier)
                else:
                    
                    dossier_nom = nom.rstrip('/') + '/'
                    if 'structure_dossiers' not in architecture:
                        architecture['structure_dossiers'] = []
                    
                    if dossier_nom not in architecture['structure_dossiers']:
                        architecture['structure_dossiers'].append(dossier_nom)
        
        architecture['fichiers'] = fichiers_filtres
        
        
        if 'structure_dossiers' not in architecture:
            architecture['structure_dossiers'] = []
        
        
        if 'point_entree' not in architecture or not architecture['point_entree']:
            
            for fichier in architecture['fichiers']:
                nom = fichier.get('nom', '')
                if any(nom.endswith(ext) for ext in ['main.py', 'main.go', 'index.js', 'app.py', 'server.js']):
                    architecture['point_entree'] = nom
                    break
            else:
                architecture['point_entree'] = 'main.py'
        
        return architecture


if __name__ == "__main__":
    print(" Test de l'Architecte MULTI-LANGAGE...")
    
    architecte = Architecte()
    
  
    test_analyses = [
        {
            "langage_principal": "go",
            "type_application": "api",
            "besoin_interface": False,
            "framework_ui": "gin",
            "description_technique": "API REST en Go avec Gin",
            "fonctionnalites_cles": ["JWT auth", "CRUD users", "PostgreSQL"],
            "dependances": []
        },
        {
            "langage_principal": "typescript",
            "type_application": "web",
            "besoin_interface": True,
            "framework_ui": "react",
            "description_technique": "Dashboard TypeScript avec React",
            "fonctionnalites_cles": ["Graphiques", "Filtres", "Tableaux"],
            "dependances": ["react", "typescript", "chart.js"]
        },
        {
            "langage_principal": "python",
            "type_application": "web",
            "besoin_interface": True,
            "framework_ui": "flask_html",
            "description_technique": "Application Flask avec interface",
            "fonctionnalites_cles": ["Formulaire", "Base de données", "API"],
            "dependances": ["Flask", "SQLAlchemy"]
        }
    ]
    
    for analyse in test_analyses:
        print(f"\n{'='*60}")
        print(f"Test {analyse['langage_principal'].upper()}: {analyse['description_technique']}")
        print(f"{'='*60}")
        
        try:
            architecture = architecte.creer_architecture(analyse)
            
            print(f"\n Architecture générée:")
            print(f"Nom projet: {architecture.get('nom_projet')}")
            print(f"Point d'entrée: {architecture.get('point_entree')}")
            
            print(f"\n Fichiers ({len(architecture.get('fichiers', []))}):")
            for fichier in architecture.get('fichiers', []):
                print(f"  - {fichier.get('nom')}: {fichier.get('description')}")
            
            print(f"\n Dossiers ({len(architecture.get('structure_dossiers', []))}):")
            for dossier in architecture.get('structure_dossiers', []):
                print(f"  - {dossier}")
                
        except Exception as e:
            print(f" Erreur: {e}")