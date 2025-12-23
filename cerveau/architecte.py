"""
🏗️ Module de conception d'architecture
Détermine la structure de fichiers pour un projet
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
        Crée une architecture de projet basée sur l'analyse
        """
        prompt = f"""
        À partir de cette analyse de projet, crée une architecture de fichiers COMPLÈTE.
        Retourne UNIQUEMENT un JSON valide.
        
        ANALYSE : {json.dumps(analyse, indent=2)}
        
        IMPORTANT : Ne pas inclure de dossiers dans la liste 'fichiers' - uniquement des fichiers.
        Les dossiers doivent aller dans 'structure_dossiers'.
        
        Retourne un JSON avec ces champs EXACTS :
        - nom_projet : nom suggéré (sans caractères spéciaux, underscore pour espaces)
        - fichiers : liste d'objets avec 'nom', 'type', 'description' (UNIQUEMENT DES FICHIERS, PAS DE DOSSIERS)
        - structure_dossiers : liste de dossiers à créer (terminés par /)
        - point_entree : nom du fichier principal (ex: main.py)
        
        EXEMPLES CORRECTS :
        FICHIERS: main.py, app.py, models.py, requirements.txt
        DOSSIERS: templates/, static/, models/, routes/
        
        EXEMPLE INCORRECT :
        FICHIERS: templates/ (← c'est un dossier, pas un fichier!)
        
        Pour une application web Flask typique :
        - FICHIERS: main.py, app.py, models.py, forms.py, config.py, requirements.txt
        - DOSSIERS: templates/, static/, instance/
        
        Le nom des fichiers doit être VALIDE pour Windows/Linux/Mac.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un architecte logiciel. Retourne uniquement du JSON valide. Les fichiers sont des fichiers, les dossiers sont des dossiers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Nettoyer le JSON
            content = self._nettoyer_json(content)
            
            architecture = json.loads(content)
            
            # POST-PROCESSING : Filtrer pour enlever les dossiers de la liste fichiers
            architecture = self._filtrer_architecture(architecture)
            
            return architecture
            
        except Exception as e:
            print(f"Erreur création architecture: {e}")
            # Architecture par défaut
            return self._architecture_par_defaut(analyse)
    
    def _nettoyer_json(self, content):
        """Nettoie le JSON retourné par l'API"""
        # Enlever les backticks de code
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        
        # Supprimer les notes ou explications
        lines = content.split('\n')
        json_lines = []
        in_json = True
        
        for line in lines:
            if line.strip().startswith('//') or line.strip().startswith('#'):
                continue  # Ignorer les commentaires
            if line.strip() == '':
                continue  # Ignorer les lignes vides
            json_lines.append(line)
        
        return '\n'.join(json_lines)
    
    def _filtrer_architecture(self, architecture):
        """Filtre l'architecture pour enlever les dossiers de la liste fichiers"""
        if 'fichiers' not in architecture:
            architecture['fichiers'] = []
        
        # Filtrer les fichiers qui sont en fait des dossiers
        fichiers_filtres = []
        for fichier in architecture.get('fichiers', []):
            if isinstance(fichier, dict) and 'nom' in fichier:
                nom = fichier['nom']
                # Ne pas inclure les noms qui se terminent par / (dossiers)
                if not nom.endswith('/') and '/' not in nom.split('/')[-1:]:
                    fichiers_filtres.append(fichier)
                else:
                    # C'est un dossier, l'ajouter à structure_dossiers si pas déjà présent
                    dossier_nom = nom.rstrip('/') + '/'
                    if 'structure_dossiers' not in architecture:
                        architecture['structure_dossiers'] = []
                    
                    # Normaliser le nom de dossier
                    if dossier_nom not in architecture['structure_dossiers']:
                        architecture['structure_dossiers'].append(dossier_nom)
        
        architecture['fichiers'] = fichiers_filtres
        
        # S'assurer que structure_dossiers existe et est une liste
        if 'structure_dossiers' not in architecture:
            architecture['structure_dossiers'] = []
        
        # Ajouter des dossiers communs basés sur l'analyse
        if not architecture['structure_dossiers']:
            architecture['structure_dossiers'] = self._generer_dossiers_par_defaut(architecture)
        
        # S'assurer que point_entree existe
        if 'point_entree' not in architecture:
            architecture['point_entree'] = 'main.py'
        
        return architecture
    
    def _generer_dossiers_par_defaut(self, architecture):
        """Génère des dossiers par défaut basés sur l'architecture"""
        dossiers = []
        
        # Vérifier les types de fichiers pour déterminer les dossiers nécessaires
        fichiers_py = [f for f in architecture.get('fichiers', []) if f.get('nom', '').endswith('.py')]
        fichiers_html = [f for f in architecture.get('fichiers', []) if f.get('nom', '').endswith('.html')]
        fichiers_css = [f for f in architecture.get('fichiers', []) if f.get('nom', '').endswith('.css')]
        
        if fichiers_html or 'templates' in [f.get('nom', '') for f in architecture.get('fichiers', [])]:
            dossiers.append('templates/')
        
        if fichiers_css or any('static' in f.get('nom', '') for f in architecture.get('fichiers', [])):
            dossiers.append('static/')
        
        # Dossiers communs
        if fichiers_py:
            dossiers.append('models/')
            dossiers.append('utils/')
        
        return dossiers
    
    def _architecture_par_defaut(self, analyse):
        """Retourne une architecture par défaut en cas d'erreur"""
        type_app = analyse.get('type_application', 'web')
        besoin_interface = analyse.get('besoin_interface', False)
        type_interface = analyse.get('type_interface', '')
        
        # Architecture de base
        architecture = {
            "nom_projet": "mon_projet",
            "fichiers": [
                {"nom": "main.py", "type": "code", "description": "Point d'entrée principal"},
                {"nom": "requirements.txt", "type": "config", "description": "Dépendances Python"},
                {"nom": "README.md", "type": "documentation", "description": "Documentation du projet"}
            ],
            "structure_dossiers": [],
            "point_entree": "main.py"
        }
        
        # Adapter selon le type d'application
        if type_app == 'web' and besoin_interface and type_interface == 'web_gui':
            architecture['fichiers'].extend([
                {"nom": "app.py", "type": "code", "description": "Application Flask principale"},
                {"nom": "models.py", "type": "code", "description": "Modèles de données"},
                {"nom": "templates/index.html", "type": "template", "description": "Template HTML principal"},
                {"nom": "static/style.css", "type": "style", "description": "Feuille de style CSS"}
            ])
            architecture['structure_dossiers'] = ['templates/', 'static/', 'models/', 'instance/']
        
        elif type_app == 'dashboard':
            architecture['fichiers'].extend([
                {"nom": "app.py", "type": "code", "description": "Application dashboard"},
                {"nom": "dashboard.py", "type": "code", "description": "Logique du dashboard"},
                {"nom": "data_processor.py", "type": "code", "description": "Traitement des données"},
                {"nom": "templates/dashboard.html", "type": "template", "description": "Template du dashboard"},
                {"nom": "static/dashboard.css", "type": "style", "description": "Style du dashboard"}
            ])
            architecture['structure_dossiers'] = ['templates/', 'static/', 'data/', 'utils/']
        
        elif type_app == 'jeu':
            architecture['fichiers'].extend([
                {"nom": "game.py", "type": "code", "description": "Logique principale du jeu"},
                {"nom": "player.py", "type": "code", "description": "Gestion du joueur"},
                {"nom": "config.py", "type": "config", "description": "Configuration du jeu"}
            ])
            if besoin_interface:
                architecture['fichiers'].append({"nom": "ui.py", "type": "code", "description": "Interface utilisateur"})
                architecture['structure_dossiers'] = ['assets/', 'sounds/', 'images/']
        
        # Filtrer les fichiers (post-processing)
        architecture = self._filtrer_architecture(architecture)
        
        return architecture

# Test rapide
if __name__ == "__main__":
    print("🧪 Test de l'Architecte...")
    
    architecte = Architecte()
    
    # Test avec une analyse simulée
    analyse_test = {
        "type_application": "dashboard",
        "besoin_interface": True,
        "type_interface": "web_gui",
        "composants_ui_attendus": ["cartes", "graphiques", "tableaux"],
        "fonctionnalites_cles": ["Visualisation données", "Filtrage", "Export"],
        "description_technique": "Dashboard interactif de visualisation de données"
    }
    
    print(f"\n📊 Analyse de test:")
    print(json.dumps(analyse_test, indent=2))
    
    print(f"\n🏗️  Génération de l'architecture...")
    architecture = architecte.creer_architecture(analyse_test)
    
    print(f"\n📁 Architecture générée:")
    print(f"Nom projet: {architecture.get('nom_projet')}")
    print(f"Point d'entrée: {architecture.get('point_entree')}")
    
    print(f"\n📄 Fichiers ({len(architecture.get('fichiers', []))}):")
    for fichier in architecture.get('fichiers', []):
        print(f"  - {fichier.get('nom')}: {fichier.get('description')}")
    
    print(f"\n📂 Dossiers ({len(architecture.get('structure_dossiers', []))}):")
    for dossier in architecture.get('structure_dossiers', []):
        print(f"  - {dossier}")
    
    # Vérifier qu'aucun dossier n'est dans la liste fichiers
    fichiers = architecture.get('fichiers', [])
    for fichier in fichiers:
        nom = fichier.get('nom', '')
        if nom.endswith('/'):
            print(f"\n⚠️  ATTENTION: Dossier trouvé dans fichiers: {nom}")