"""
🧠 Module d'analyse COMPLÈTE des demandes utilisateur
Version avec DÉTECTION MANUELLE FORCÉE - Pas d'API pour Go, Java, Django, etc.
"""

import json
import os
import re
from groq import Groq
from dotenv import load_dotenv

# Charger .env
load_dotenv()

class AnalysateurAvance:
    def __init__(self):
    
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY non trouvée dans .env")
        
        print(f"Initialisation API Groq...")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        print(f"   → Modèle : {self.model}")
    
    def analyser_demande(self, demande):
        """
        Analyse COMPLÈTE avec DÉTECTION MANUELLE FORCÉE
        PAS D'API pour les langages spécifiques !
        """
        print(f" Analyse intelligente : {demande[:60]}...")
        
        demande_lower = demande.lower()
        
        # ============ DÉTECTION MANUELLE FORCÉE ============
        # Go - PRIORITÉ ABSOLUE
        if any(mot in demande_lower for mot in ['go ', 'golang', 'gqlgen', '.go', 'func ', 'package ', 'fmt.println']):
            print(f"   Détection FORCÉE: GO")
            return self._generer_analyse_go(demande, demande_lower)
        
        # Django
        if 'django' in demande_lower:
            print(f"   Détection FORCÉE: DJANGO")
            return self._generer_analyse_django(demande, demande_lower)
        
        # Java/Spring Boot
        if any(mot in demande_lower for mot in ['java', 'spring', 'spring boot', 'spring-boot', 'jpa', 'hibernate']):
            print(f"    Détection FORCÉE: JAVA")
            return self._generer_analyse_java(demande, demande_lower)
        
        # Rust
        if 'rust' in demande_lower or '.rs' in demande_lower:
            print(f"    Détection FORCÉE: RUST")
            return self._generer_analyse_rust(demande, demande_lower)
        
        # Python Flask/Streamlit
        if 'flask' in demande_lower or 'streamlit' in demande_lower:
            print(f"    Détection FORCÉE: PYTHON")
            return self._generer_analyse_python(demande, demande_lower)
        
        # TypeScript/React/Node.js
        if any(mot in demande_lower for mot in ['typescript', 'javascript', 'react', 'vue', 'angular', 'node.js', 'express']):
            print(f"     Détection FORCÉE: TYPESCRIPT/JAVASCRIPT")
            return self._generer_analyse_typescript(demande, demande_lower)
        
        # Si aucun langage spécifique détecté, utiliser l'API
        print("    Appel à l'API Groq (langage non spécifique)...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un architecte logiciel. Retourne uniquement du JSON."},
                    {"role": "user", "content": f"Analyse: {demande}"}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            content = content.strip()
            
            print(f"    Réponse API reçue ({len(content)} caractères)")
            
            content = self._nettoyer_reponse_json(content)
            analyse = json.loads(content)
            
        except Exception as e:
            print(f"     Erreur API, utilisation de fallback: {e}")
            analyse = self._analyse_fallback(demande, demande_lower)
        
        # Afficher les résultats
        print(f"    Analyse COMPLÈTE terminée :")
        print(f"      Type projet: {analyse.get('type_projet', 'N/A').upper()}")
        print(f"      Type: {analyse.get('type_application')}")
        print(f"      Langage: {analyse.get('langage_principal', 'N/A').upper()}")
        print(f"      Interface: {'' if analyse.get('besoin_interface') else ''} {analyse.get('type_interface')}")
        
        if analyse.get('type_projet') == 'fullstack':
            print(f"        FRONTEND: {', '.join(analyse.get('technologies_frontend', []))}")
            print(f"       BACKEND: {', '.join(analyse.get('technologies_backend', []))}")
            print(f"       DATABASE: {', '.join(analyse.get('base_de_donnees', []))}")
        
        if analyse.get('besoin_interface'):
            print(f"       Composants UI: {', '.join(analyse.get('composants_ui_attendus', []))}")
        print(f"       Fonctionnalités: {len(analyse.get('fonctionnalites_cles', []))} clés")
        
        return analyse
    
    def _generer_analyse_go(self, demande, demande_lower):
        """Génère une analyse spécifique pour Go"""
        print(f"    Détection projet: BACKEND (Go API)")
        print(f"     Configuration projet BACKEND détectée")
        
        type_projet = 'backend'
        besoin_interface = False
        
       
        if any(mot in demande_lower for mot in ['react', 'vue', 'angular', 'frontend']):
            type_projet = 'fullstack'
            besoin_interface = True
        
        return {
            "type_application": "api",
            "type_projet": type_projet,
            "besoin_interface": besoin_interface,
            "type_interface": "web_gui" if besoin_interface else "aucune",
            "complexite_interface": "complexe",
            "composants_ui_attendus": ["graphiques", "tableaux"] if besoin_interface else [],
            "technologies_frontend": ["react", "typescript"] if 'react' in demande_lower else [],
            "technologies_backend": self._detecter_technologies_backend_go(demande_lower),
            "base_de_donnees": self._detecter_bases_donnees(demande_lower),
            "authentification": self._detecter_authentification(demande_lower),
            "langage_backend": "go",
            "langage_principal": "go",
            "framework_ui": "gqlgen" if 'gqlgen' in demande_lower else "gin",
            "description_technique": f"API Go basée sur: {demande[:100]}...",
            "fonctionnalites_cles": self._extraire_fonctionnalites_go(demande_lower),
            "dependances": self._generer_dependances_go(demande_lower),
            "deploiement": self._detecter_deploiement(demande_lower)
        }
    
    def _detecter_technologies_backend_go(self, demande_lower):
        """Détecte les technologies backend spécifiques à Go"""
        techs = []
        
        if 'gin' in demande_lower:
            techs.append('gin')
        elif 'echo' in demande_lower:
            techs.append('echo')
        elif 'fiber' in demande_lower:
            techs.append('fiber')
        else:
            techs.append('gin')  # Par défaut
            
        if 'gqlgen' in demande_lower:
            techs.append('gqlgen')
        elif 'graphql' in demande_lower:
            techs.append('graphql-go')
            
      
        if 'websocket' in demande_lower or 'subscription' in demande_lower:
            techs.append('websocket')
            
        return techs
    
    def _generer_dependances_go(self, demande_lower):
        """Génère les dépendances Go"""
        dependances = []
        
        
        if 'gin' in demande_lower:
            dependances.append('github.com/gin-gonic/gin')
        elif 'echo' in demande_lower:
            dependances.append('github.com/labstack/echo/v4')
        elif 'fiber' in demande_lower:
            dependances.append('github.com/gofiber/fiber/v2')
        else:
            dependances.append('github.com/gin-gonic/gin')  
        
        
        if 'gqlgen' in demande_lower:
            dependances.extend([
                'github.com/99designs/gqlgen',
                'github.com/vektah/gqlparser/v2'
            ])
        elif 'graphql' in demande_lower:
            dependances.append('github.com/graph-gophers/graphql-go')
        
      
        if 'websocket' in demande_lower or 'subscription' in demande_lower:
            dependances.extend([
                'github.com/gorilla/websocket',
                'nhooyr.io/websocket'
            ])
        
        if 'postgresql' in demande_lower or 'postgres' in demande_lower:
            dependances.extend([
                'github.com/jackc/pgx/v5',
                'github.com/go-pg/pg/v10',
                'github.com/jinzhu/gorm'
            ])
        
        
        if 'jwt' in demande_lower:
            dependances.extend([
                'github.com/golang-jwt/jwt/v5',
                'github.com/auth0/go-jwt-middleware'
            ])
        
        
        dependances.append('github.com/rs/cors')
        
        
        dependances.append('github.com/joho/godotenv')
        
        if 'kubernetes' in demande_lower or 'k8s' in demande_lower:
            dependances.extend([
                'k8s.io/client-go',
                'k8s.io/apimachinery'
            ])
        
        
        dependances.append('github.com/sirupsen/logrus')
        
       
        dependances.append('github.com/go-playground/validator/v10')
        
        return dependances
    
    def _extraire_fonctionnalites_go(self, demande_lower):
        """Extrait les fonctionnalités spécifiques à Go"""
        fonctionnalites = []
        
        if 'graphql' in demande_lower:
            fonctionnalites.append("API GraphQL")
        if 'postgresql' in demande_lower:
            fonctionnalites.append("Base de données PostgreSQL")
        if 'jwt' in demande_lower:
            fonctionnalites.append("Authentification JWT")
        if 'websocket' in demande_lower:
            fonctionnalites.append("Subscriptions WebSocket")
        if 'kubernetes' in demande_lower:
            fonctionnalites.append("Déploiement Kubernetes")
        if 'subscription' in demande_lower:
            fonctionnalites.append("Subscriptions en temps réel")
        
        if not fonctionnalites:
            fonctionnalites = ["API Go", "Performance élevée", "Concurrence native"]
        
        return fonctionnalites
    
    def _generer_analyse_django(self, demande, demande_lower):
        """Génère une analyse spécifique pour Django"""
        return {
            "type_application": "web",
            "type_projet": "backend",
            "besoin_interface": True,
            "type_interface": "web_gui",
            "complexite_interface": "complexe",
            "composants_ui_attendus": ["formulaires", "tableaux", "dashboard"],
            "technologies_frontend": [],
            "technologies_backend": ["django"],
            "base_de_donnees": ["postgresql"] if 'postgresql' in demande_lower else ["sqlite"],
            "authentification": ["session"],
            "langage_backend": "python",
            "langage_principal": "python",
            "framework_ui": "django",
            "description_technique": f"Application Django basée sur: {demande[:100]}...",
            "fonctionnalites_cles": ["Interface admin", "Authentification", "API REST"],
            "dependances": self._generer_dependances_django(demande_lower),
            "deploiement": ["docker"]
        }
    
    def _generer_analyse_java(self, demande, demande_lower):
        """Génère une analyse spécifique pour Java"""
        return {
            "type_application": "api",
            "type_projet": "backend",
            "besoin_interface": False,
            "type_interface": "aucune",
            "complexite_interface": "complexe",
            "composants_ui_attendus": [],
            "technologies_frontend": [],
            "technologies_backend": ["spring", "spring-boot"],
            "base_de_donnees": self._detecter_bases_donnees(demande_lower),
            "authentification": self._detecter_authentification(demande_lower),
            "langage_backend": "java",
            "langage_principal": "java",
            "framework_ui": "spring-boot",
            "description_technique": f"API Spring Boot basée sur: {demande[:100]}...",
            "fonctionnalites_cles": ["API REST", "Sécurité", "Performance"],
            "dependances": self._generer_dependances_spring_boot(demande_lower),
            "deploiement": ["docker", "kubernetes"]
        }
    
    def _generer_analyse_rust(self, demande, demande_lower):
        """Génère une analyse spécifique pour Rust"""
        return {
            "type_application": "api",
            "type_projet": "backend",
            "besoin_interface": False,
            "type_interface": "aucune",
            "complexite_interface": "complexe",
            "composants_ui_attendus": [],
            "technologies_frontend": [],
            "technologies_backend": ["actix-web"],
            "base_de_donnees": self._detecter_bases_donnees(demande_lower),
            "authentification": self._detecter_authentification(demande_lower),
            "langage_backend": "rust",
            "langage_principal": "rust",
            "framework_ui": "actix",
            "description_technique": f"API Rust basée sur: {demande[:100]}...",
            "fonctionnalites_cles": ["Performance", "Sécurité mémoire", "Concurrence"],
            "dependances": self._generer_dependances_rust(demande_lower),
            "deploiement": ["docker"]
        }
    
    def _generer_analyse_python(self, demande, demande_lower):
        """Génère une analyse spécifique pour Python (Flask/Streamlit)"""
        if 'streamlit' in demande_lower:
            framework = "streamlit"
            type_app = "streamlit"
            besoin_interface = True
            type_interface = "streamlit_gui"
        else:
            framework = "flask_html"
            type_app = "web"
            besoin_interface = True
            type_interface = "web_gui"
        
        return {
            "type_application": type_app,
            "type_projet": "web",
            "besoin_interface": besoin_interface,
            "type_interface": type_interface,
            "complexite_interface": "moyenne",
            "composants_ui_attendus": self._detecter_composants_ui(demande_lower),
            "technologies_frontend": [],
            "technologies_backend": ["flask"] if 'flask' in demande_lower else [],
            "base_de_donnees": [],
            "authentification": [],
            "langage_backend": "python",
            "langage_principal": "python",
            "framework_ui": framework,
            "description_technique": f"Application Python basée sur: {demande[:100]}...",
            "fonctionnalites_cles": self._extraire_fonctionnalites(demande),
            "dependances": self._generer_dependances_python(demande_lower),
            "deploiement": []
        }
    
    def _generer_analyse_typescript(self, demande, demande_lower):
        """Génère une analyse spécifique pour TypeScript/JavaScript"""
        type_projet = 'fullstack' if any(mot in demande_lower for mot in ['frontend', 'react', 'vue', 'angular']) else 'backend'
        besoin_interface = type_projet == 'fullstack'
        
        return {
            "type_application": "web",
            "type_projet": type_projet,
            "besoin_interface": besoin_interface,
            "type_interface": "web_gui" if besoin_interface else "aucune",
            "complexite_interface": "moyenne",
            "composants_ui_attendus": self._detecter_composants_ui(demande_lower),
            "technologies_frontend": ["react", "typescript"] if 'react' in demande_lower else ["javascript"],
            "technologies_backend": ["express", "node.js"],
            "base_de_donnees": self._detecter_bases_donnees(demande_lower),
            "authentification": self._detecter_authentification(demande_lower),
            "langage_backend": "javascript",
            "langage_principal": "typescript",
            "framework_ui": "react" if 'react' in demande_lower else "vanilla",
            "description_technique": f"Application TypeScript basée sur: {demande[:100]}...",
            "fonctionnalites_cles": self._extraire_fonctionnalites(demande),
            "dependances": self._generer_dependances_typescript(demande_lower),
            "deploiement": ["vercel", "heroku"]
        }
    
    def _generer_dependances_typescript(self, demande_lower):
        """Génère les dépendances TypeScript"""
        dependances = []
        
        
        if 'express' in demande_lower or 'node.js' in demande_lower:
            dependances.extend(['express', 'cors', '@types/express'])
        
       
        if 'react' in demande_lower:
            dependances.extend(['react', 'react-dom', '@types/react'])
        
        
        dependances.extend(['typescript', '@types/node', 'ts-node'])
        
       
        if 'mongodb' in demande_lower:
            dependances.append('mongoose')
        elif 'postgresql' in demande_lower:
            dependances.extend(['pg', '@types/pg'])
        
        
        if 'jwt' in demande_lower:
            dependances.extend(['jsonwebtoken', '@types/jsonwebtoken', 'bcryptjs'])
        
        
        if 'graphql' in demande_lower:
            dependances.extend(['graphql', 'apollo-server', '@apollo/client'])
        
        return dependances
    
    def _analyse_fallback(self, demande, demande_lower):
        """Analyse de fallback générique"""
        return {
            "type_application": "web",
            "type_projet": "web",
            "besoin_interface": True,
            "type_interface": "web_gui",
            "complexite_interface": "moyenne",
            "composants_ui_attendus": ["formulaires", "tableaux"],
            "technologies_frontend": [],
            "technologies_backend": [],
            "base_de_donnees": [],
            "authentification": [],
            "langage_backend": "python",
            "langage_principal": "python",
            "framework_ui": "flask_html",
            "description_technique": f"Application basée sur: {demande[:100]}...",
            "fonctionnalites_cles": self._extraire_fonctionnalites(demande),
            "dependances": ["Flask"],
            "deploiement": []
        }
    
    
    
    def _nettoyer_reponse_json(self, content):
        """Nettoie le JSON"""
       
        start = content.find('{')
        end = content.rfind('}') + 1
        
        if start != -1 and end != 0:
            content = content[start:end]
        
        content = content.replace('```json', '').replace('```', '').strip()
        
        try:
            json.loads(content)
            return content
        except:
            return self._reparer_json(content)
    
    def _reparer_json(self, content):
        """Tente de réparer un JSON malformé"""
        content = re.sub(r'[\x00-\x1F\x7F]', '', content)
        
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            content = match.group(0)
        
        if "'" in content and '"' not in content:
            content = content.replace("'", '"')
        
        content = re.sub(r'(\w+):', r'"\1":', content)
        
        return content
    
    def _detecter_bases_donnees(self, demande_lower):
        """Détecte les bases de données mentionnées"""
        databases = []
        db_techs = ['mongodb', 'postgresql', 'mysql', 'sqlite', 'redis', 'firebase', 'supabase']
        
        for db in db_techs:
            if db in demande_lower and db not in databases:
                databases.append(db)
        
        return databases
    
    def _detecter_authentification(self, demande_lower):
        """Détecte les méthodes d'authentification mentionnées"""
        auth_methods = []
        auth_techs = ['jwt', 'oauth', 'session', 'basic auth', 'firebase auth', 'auth0']
        
        for auth in auth_techs:
            if auth in demande_lower and auth not in auth_methods:
                auth_methods.append(auth)
        
        return auth_methods
    
    def _detecter_deploiement(self, demande_lower):
        """Détecte les plateformes de déploiement mentionnées"""
        deploiement = []
        deploiement_techs = ['vercel', 'heroku', 'aws', 'docker', 'kubernetes', 'netlify', 'railway']
        
        for dep in deploiement_techs:
            if dep in demande_lower and dep not in deploiement:
                deploiement.append(dep)
        
        return deploiement
    
    def _detecter_composants_ui(self, demande_lower):
        """Détecte les composants UI mentionnés"""
        composants = []
        mapping = {
            'carte': 'cartes',
            'card': 'cartes',
            'formulaire': 'formulaires',
            'form': 'formulaires',
            'tableau': 'tableaux',
            'liste': 'tableaux',
            'table': 'tableaux',
            'graphique': 'graphiques',
            'chart': 'graphiques',
            'statistique': 'graphiques',
            'dashboard': 'dashboard',
            'jeu': 'jeu',
            'game': 'jeu',
            'calcul': 'calculatrice',
            'calculator': 'calculatrice',
            'galerie': 'galerie',
            'gallery': 'galerie'
        }
        
        for mot, composant in mapping.items():
            if mot in demande_lower and composant not in composants:
                composants.append(composant)
        
        return composants
    
    def _generer_dependances_django(self, demande_lower):
        """Génère les dépendances Django"""
        dependances = [
            'django',
            'djangorestframework',
            'django-cors-headers'
        ]
        
        if 'postgresql' in demande_lower or 'postgres' in demande_lower:
            dependances.append('psycopg2-binary')
        elif 'mysql' in demande_lower:
            dependances.append('mysqlclient')
        
        if 'upload' in demande_lower or 'image' in demande_lower:
            dependances.append('Pillow')
        
        if 'deploiement' in demande_lower or 'docker' in demande_lower:
            dependances.extend(['gunicorn', 'whitenoise'])
        
        if 'jwt' in demande_lower:
            dependances.append('djangorestframework-simplejwt')
        
        return dependances
    
    def _generer_dependances_spring_boot(self, demande_lower):
        """Génère les dépendances Spring Boot"""
        dependances = [
            'spring-boot-starter-web',
            'spring-boot-starter-data-jpa',
            'spring-boot-starter-test',
            'spring-boot-devtools'
        ]
        
        if 'postgresql' in demande_lower or 'postgres' in demande_lower:
            dependances.append('postgresql')
        elif 'mysql' in demande_lower:
            dependances.append('mysql-connector-java')
        elif 'mongodb' in demande_lower:
            dependances.append('spring-boot-starter-data-mongodb')
        else:
            dependances.append('h2')
        
        if 'jwt' in demande_lower:
            dependances.extend(['jjwt-api', 'jjwt-impl', 'jjwt-jackson'])
        
        if 'swagger' in demande_lower:
            dependances.extend(['springdoc-openapi-starter-webmvc-ui'])
        
        if 'lombok' in demande_lower:
            dependances.append('lombok')
        
        return dependances
    
    def _generer_dependances_rust(self, demande_lower):
        """Génère les dépendances Rust"""
        dependances = []
        
        if 'actix' in demande_lower:
            dependances.extend(['actix-web', 'actix-rt'])
        elif 'rocket' in demande_lower:
            dependances.extend(['rocket', 'rocket_dyn_templates'])
        else:
            dependances.extend(['actix-web', 'actix-rt'])
        
        if 'graphql' in demande_lower:
            dependances.extend(['async-graphql', 'async-graphql-actix-web'])
        
        if 'postgresql' in demande_lower:
            dependances.extend(['sqlx', 'postgres'])
        
        if 'jwt' in demande_lower:
            dependances.extend(['jsonwebtoken', 'chrono'])
        
        if 'websocket' in demande_lower:
            dependances.extend(['tokio-tungstenite', 'futures'])
        
        dependances.extend(['serde', 'serde_json'])
        
        return dependances
    
    def _generer_dependances_python(self, demande_lower):
        """Génère les dépendances Python"""
        dependances = []
        
        if 'flask' in demande_lower:
            dependances.append('Flask')
        elif 'streamlit' in demande_lower:
            dependances.append('streamlit')
        
        if 'pandas' in demande_lower:
            dependances.append('pandas')
        
        if 'plot' in demande_lower or 'graph' in demande_lower:
            dependances.append('matplotlib')
        
        return dependances
    
    def _extraire_fonctionnalites(self, demande):
        """Extrait les fonctionnalités clés"""
        mots_cles = [
            "ajouter", "supprimer", "modifier", "rechercher", "filtrer", "trier",
            "afficher", "calculer", "convertir", "enregistrer", "importer", "exporter",
            "télécharger", "uploader", "partager", "commenter", "noter", "voter",
            "comparer", "analyser", "statistique", "graphique", "rapport", "dashboard",
            "visualiser", "voir", "montrer", "présenter", "tableau"
        ]
        
        fonctionnalites = []
        demande_lower = demande.lower()
        
        for mot in mots_cles:
            if mot in demande_lower:
                fonctionnalites.append(mot)
        
        if not fonctionnalites:
            fonctionnalites = ["fonctionnalite_principale"]
        
        return fonctionnalites



if __name__ == "__main__":
    print(" Test de l'analyseur FORCÉ FINAL...")
    
    analyseur = AnalysateurAvance()
    
    test_demandes = [
        "API GraphQL en Go avec Gqlgen, base de données PostgreSQL, authentification JWT, subscriptions WebSocket, et déploiement sur Kubernetes",
        "Application web Django avec PostgreSQL et API REST",
        "API Spring Boot avec MongoDB et JWT",
        "Application React avec Node.js backend et MongoDB"
    ]
    
    for demande in test_demandes:
        print(f"\n{'='*80}")
        print(f"Test : {demande}")
        print(f"{'='*80}")
        
        try:
            analyse = analyseur.analyser_demande(demande)
            print(f"\n RÉSULTAT D'ANALYSE :")
            print(f"  Langage: {analyse.get('langage_principal', 'N/A').upper()}")
            print(f"  Type projet: {analyse.get('type_projet', 'N/A').upper()}")
            print(f"  Type app: {analyse.get('type_application')}")
            print(f"  Framework: {analyse.get('framework_ui')}")
            print(f"  Backend tech: {', '.join(analyse.get('technologies_backend', []))}")
            print(f"  Database: {', '.join(analyse.get('base_de_donnees', []))}")
            print(f"  Dépendances: {', '.join(analyse.get('dependances', []))}")
            
        except Exception as e:
            print(f" Erreur: {e}")
            import traceback
            traceback.print_exc()