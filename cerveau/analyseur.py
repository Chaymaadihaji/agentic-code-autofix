"""
🧠 Module d'analyse COMPLÈTE des demandes utilisateur
Détecte automatiquement les besoins backend ET frontend
"""

import json
import os
import re
from groq import Groq
from dotenv import load_dotenv

# Charger .env
load_dotenv()

class Analyser:
    def __init__(self):
        # Vérifier que la clé API est disponible
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY non trouvée dans .env")
        
        print(f"🔑 Initialisation API Groq...")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        print(f"   → Modèle : {self.model}")
    
    def analyser_demande(self, demande):
        """
        Analyse COMPLÈTE pour déterminer les besoins backend + frontend
        """
        print(f"🧠 Analyse intelligente : {demande[:60]}...")
        
        prompt = f"""
        Analyse cette demande de développement et identifie TOUS les besoins techniques.
        
        DEMANDE ORIGINALE : "{demande}"
        
        Questions critiques à analyser :
        1. Cette application nécessite-t-elle une interface utilisateur (UI) ?
        2. Si oui, quel type d'interface (CLI simple, web GUI, desktop, mobile) ?
        3. Quels composants UI sont attendus (cartes, formulaires, tableaux, graphiques, galerie, dashboard, etc.) ?
        4. Quelle est la complexité technique globale ?
        5. Quelles sont les fonctionnalités clés à implémenter ?
        6. Quel est le langage backend le plus adapté ?
        
        IMPORTANT : Évalue objectivement. Même une calculatrice simple a besoin d'une interface.
        
        Retourne UNIQUEMENT et EXACTEMENT ce JSON (pas d'autres texte) :
        {{
            "type_application": "web|desktop|mobile|cli|api|jeu|utilitaire|dashboard|autre",
            "besoin_interface": true|false,
            "type_interface": "web_gui|desktop_gui|mobile_gui|cli|aucune",
            "complexite_interface": "simple|moyenne|complexe",
            "composants_ui_attendus": ["cartes", "formulaires", "tableaux", "graphiques", "galerie", "dashboard", "jeu", "calculatrice", "visualisation", "autre"],
            "langage_backend": "python|javascript|autre",
            "framework_ui": "flask_html|streamlit|tkinter|autre",
            "description_technique": "description courte et précise de ce que doit faire l'application",
            "fonctionnalites_cles": ["liste des fonctionnalités principales à implémenter"],
            "dependances": ["Flask", "autres dépendances probables selon le type d'application"]
        }}
        
        Exemples de décisions :
        - "calculatrice" → besoin_interface:true, type_interface:web_gui, composants:["calculatrice"]
        - "site web météo" → besoin_interface:true, type_interface:web_gui, composants:["cartes", "graphiques"]
        - "todo list" → besoin_interface:true, type_interface:web_gui, composants:["formulaires", "tableaux"]
        - "api de données" → besoin_interface:false, type_interface:aucune
        - "jeu de memory" → besoin_interface:true, type_interface:web_gui, composants:["jeu", "cartes"]
        """
        
        try:
            print("   📡 Appel à l'API Groq pour analyse complète...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un architecte logiciel expert. Analyse les besoins techniques objectivement et retourne uniquement du JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Plus bas pour plus de consistance
                max_tokens=600
            )
            
            # Extraire le JSON de la réponse
            content = response.choices[0].message.content
            content = content.strip()
            
            print(f"   ✅ Réponse API reçue ({len(content)} caractères)")
            
            # Nettoyer la réponse agressivement
            content = self._nettoyer_reponse_json(content)
            
            analyse = json.loads(content)
            
            # Validation et normalisation des champs
            analyse = self._valider_et_normaliser_analyse(analyse, demande)
            
            print(f"   📊 Analyse COMPLÈTE terminée :")
            print(f"      Type: {analyse.get('type_application')}")
            print(f"      Interface: {'✅' if analyse.get('besoin_interface') else '❌'} {analyse.get('type_interface')}")
            if analyse.get('besoin_interface'):
                print(f"      Composants UI: {', '.join(analyse.get('composants_ui_attendus', []))}")
            print(f"      Fonctionnalités: {len(analyse.get('fonctionnalites_cles', []))} clés")
            
            return analyse
            
        except json.JSONDecodeError as e:
            print(f"❌ Erreur de parsing JSON : {e}")
            print(f"Contenu problématique : {content[:300]}...")
            return self._analyse_par_defaut_ameliorée(demande)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            import traceback
            traceback.print_exc()
            return self._analyse_par_defaut_ameliorée(demande)
    
    def _nettoyer_reponse_json(self, content):
        """Nettoie agressivement la réponse pour extraire le JSON"""
        # Chercher le premier { et le dernier }
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start != -1 and end != 0:
            content = content[start:end]
        
        # Enlever les blocs de code
        content = content.replace('```json', '').replace('```', '')
        
        # Enlever les espaces/tabulations extrêmes
        content = content.strip()
        
        # Valider que c'est du JSON
        try:
            json.loads(content)  # Test de validation
            return content
        except:
            # Essayer de réparer le JSON
            return self._reparer_json(content)
    
    def _reparer_json(self, content):
        """Tente de réparer un JSON malformé"""
        # Enlever les caractères problématiques
        content = re.sub(r'[\x00-\x1F\x7F]', '', content)
        
        # Essayer d'extraire un objet JSON
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            content = match.group(0)
        
        # Remplacer les guillemets simples par doubles si nécessaire
        if "'" in content and '"' not in content:
            content = content.replace("'", '"')
        
        # Ajouter des guillemets manquants aux clés
        content = re.sub(r'(\w+):', r'"\1":', content)
        
        return content
    
    def _valider_et_normaliser_analyse(self, analyse, demande):
        """Valide et normalise l'analyse pour la cohérence"""
        # Champs obligatoires
        defaults = {
            "type_application": "web",
            "besoin_interface": True,
            "type_interface": "web_gui",
            "complexite_interface": "moyenne",
            "composants_ui_attendus": [],
            "langage_backend": "python",
            "framework_ui": "flask_html",
            "description_technique": f"Application basée sur: {demande[:80]}...",
            "fonctionnalites_cles": ["fonctionnalite_principale"],
            "dependances": ["Flask"]
        }
        
        # Appliquer les defaults pour les champs manquants
        for key, default in defaults.items():
            if key not in analyse or analyse[key] is None:
                analyse[key] = default
        
        # Normalisation des valeurs
        if isinstance(analyse.get("composants_ui_attendus"), str):
            analyse["composants_ui_attendus"] = [analyse["composants_ui_attendus"]]
        
        if isinstance(analyse.get("fonctionnalites_cles"), str):
            analyse["fonctionnalites_cles"] = [analyse["fonctionnalites_cles"]]
        
        if isinstance(analyse.get("dependances"), str):
            analyse["dependances"] = [analyse["dependances"]]
        
        # Détection automatique basée sur la demande
        demande_lower = demande.lower()
        
        # Détection type application
        if any(mot in demande_lower for mot in ['web', 'site', 'page', 'flask', 'django']):
            analyse["type_application"] = "web"
            analyse["type_interface"] = "web_gui"
        
        elif any(mot in demande_lower for mot in ['jeu', 'game', 'jouer', 'score', 'memory', 'quiz']):
            analyse["type_application"] = "jeu"
            analyse["besoin_interface"] = True
            analyse["type_interface"] = "web_gui"
            if "jeu" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("jeu")
        
        elif any(mot in demande_lower for mot in ['dashboard', 'tableau', 'métrique', 'statistique', 'graphique']):
            analyse["type_application"] = "dashboard"
            analyse["besoin_interface"] = True
            if "graphiques" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("graphiques")
            if "dashboard" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("dashboard")
        
        elif any(mot in demande_lower for mot in ['calcul', 'math', 'addition', 'soustraction']):
            analyse["type_application"] = "utilitaire"
            analyse["besoin_interface"] = True
            if "calculatrice" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("calculatrice")
        
        # Détection composants UI
        if "carte" in demande_lower or "card" in demande_lower:
            if "cartes" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("cartes")
        
        if "formulaire" in demande_lower or "form" in demande_lower:
            if "formulaires" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("formulaires")
        
        if "tableau" in demande_lower or "liste" in demande_lower or "table" in demande_lower:
            if "tableaux" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("tableaux")
        
        if "graphique" in demande_lower or "chart" in demande_lower or "statistique" in demande_lower:
            if "graphiques" not in analyse["composants_ui_attendus"]:
                analyse["composants_ui_attendus"].append("graphiques")
        
        # S'assurer que Flask est dans les dépendances pour les apps web
        if analyse["type_application"] == "web" and "Flask" not in analyse["dependances"]:
            analyse["dependances"].append("Flask")
        
        # Pour les apps CLI, pas d'interface
        if analyse["type_interface"] == "cli":
            analyse["besoin_interface"] = False
            analyse["composants_ui_attendus"] = []
        
        return analyse
    
    def _analyse_par_defaut_ameliorée(self, demande):
        """Analyse par défaut améliorée avec détection intelligente"""
        print("⚠️  Utilisation de l'analyse par défaut améliorée")
        
        demande_lower = demande.lower()
        
        # Détection intelligente
        if any(mot in demande_lower for mot in ['web', 'site', 'page', 'flask', 'html', 'css']):
            type_app = "web"
            besoin_interface = True
            type_interface = "web_gui"
            composants = []
            dependances = ["Flask"]
            
            if "carte" in demande_lower:
                composants.append("cartes")
            if "formulaire" in demande_lower:
                composants.append("formulaires")
            if "graphique" in demande_lower:
                composants.append("graphiques")
            if "tableau" in demande_lower:
                composants.append("tableaux")
            
        elif any(mot in demande_lower for mot in ['jeu', 'game', 'memory', 'quiz', 'puzzle']):
            type_app = "jeu"
            besoin_interface = True
            type_interface = "web_gui"
            composants = ["jeu"]
            dependances = []
            
        elif any(mot in demande_lower for mot in ['api', 'rest', 'json', 'endpoint']):
            type_app = "api"
            besoin_interface = False
            type_interface = "aucune"
            composants = []
            dependances = ["Flask"]  # Pour les API REST
            
        else:
            # Par défaut, application web avec interface
            type_app = "web"
            besoin_interface = True
            type_interface = "web_gui"
            composants = []
            dependances = ["Flask"]
        
        # Extraire les fonctionnalités clés
        fonctionnalites = self._extraire_fonctionnalites(demande)
        
        return {
            "type_application": type_app,
            "besoin_interface": besoin_interface,
            "type_interface": type_interface,
            "complexite_interface": "moyenne",
            "composants_ui_attendus": composants,
            "langage_backend": "python",
            "framework_ui": "flask_html",
            "description_technique": f"Application basée sur la demande : {demande[:100]}...",
            "fonctionnalites_cles": fonctionnalites,
            "dependances": dependances
        }
    
    def _extraire_fonctionnalites(self, demande):
        """Extrait les fonctionnalités clés de la demande"""
        mots_cles_fonctionnalites = [
            "ajouter", "supprimer", "modifier", "rechercher", "filtrer", "trier",
            "afficher", "calculer", "convertir", "enregistrer", "importer", "exporter",
            "télécharger", "uploader", "partager", "commenter", "noter", "voter",
            "comparer", "analyser", "statistique", "graphique", "rapport", "dashboard"
        ]
        
        fonctionnalites = []
        demande_lower = demande.lower()
        
        for mot in mots_cles_fonctionnalites:
            if mot in demande_lower:
                fonctionnalites.append(mot)
        
        if not fonctionnalites:
            fonctionnalites = ["fonctionnalite_principale"]
        
        return fonctionnalites

# Test rapide
if __name__ == "__main__":
    print("🧪 Test de l'analyseur amélioré...")
    
    analyseur = Analyser()
    
    test_demandes = [
        "application météo avec cartes pour 5 villes et graphiques",
        "gestionnaire de contacts avec formulaire et tableau",
        "jeu de memory avec cartes animées",
        "api pour obtenir des données utilisateur en JSON",
        "calculatrice scientifique avec interface moderne"
    ]
    
    for demande in test_demandes:
        print(f"\n{'='*60}")
        print(f"Test : {demande}")
        print(f"{'='*60}")
        
        try:
            analyse = analyseur.analyser_demande(demande)
            print(f"Résultat :")
            print(f"  Type app: {analyse.get('type_application')}")
            print(f"  Interface: {analyse.get('besoin_interface')} ({analyse.get('type_interface')})")
            print(f"  Composants: {analyse.get('composants_ui_attendus')}")
            print(f"  Fonctionnalités: {analyse.get('fonctionnalites_cles')}")
            print(f"  Dépendances: {analyse.get('dependances')}")
        except Exception as e:
            print(f"❌ Erreur: {e}")