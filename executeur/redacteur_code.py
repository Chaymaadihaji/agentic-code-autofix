"""
 Module de génération de code MULTI-LANGAGE avec APPRENTISSAGE INTELLIGENT
Génère du code et apprend de ses erreurs pour améliorer les futures générations
"""

import os
import json
import time
import hashlib
import random
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


try:
    from cerveau.apprentissage import MemoireApprentissage
    from executeur.correcteur import CorrecteurIntelligent
except ImportError as e:
    print(f" Import apprentissage échoué: {e}")
    print(" Création des classes minimales pour l'apprentissage...")
    
    
    class MemoireApprentissage:
        def __init__(self, fichier_memoire="memoire_apprentissage.json"):
            self.fichier_memoire = fichier_memoire
            self.corrections_apprises = []
            print(" Mémoire d'apprentissage initialisée (mode minimal)")
        
        def enregistrer_erreur(self, erreur):
            self.corrections_apprises.append(erreur)
            return f"err_{len(self.corrections_apprises)}"
        
        def trouver_corrections_similaires(self, erreur):
            return []
        
        def appliquer_corrections_connues(self, code, langage, fichier):
            return code
        
        def get_statistiques(self):
            return {"total_corrections": len(self.corrections_apprises)}
        
        def reset_session(self):
            pass
    
    class CorrecteurIntelligent:
        def __init__(self, memoire):
            self.memoire = memoire
            self.corrections_appliquees = []
        
        def corriger_code(self, code, langage, fichier, tentative, projet):
            return code, []
        
        def get_rapport_correction(self):
            return "Système de correction minimal"
        
        def reset_corrections(self):
            self.corrections_appliquees = []

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
        self.cache = CacheAPI()
        
       
        self.test_mode = False
        self.tentative_num = 0
        self.projet_courant = ""
        self.langage_courant = ""
        
       
        self.memoire = MemoireApprentissage()
        self.correcteur = CorrecteurIntelligent(self.memoire)
        self.erreurs_apprises = []
        
        print(f" Rédacteur avec apprentissage initialisé - {self.memoire.get_statistiques().get('total_corrections', 0)} corrections apprises")
    
    def set_test_mode(self, test_mode, tentative_num):
        """Active/désactive le mode test avec bugs"""
        self.test_mode = test_mode
        self.tentative_num = tentative_num
        print(f"    Mode test: {'ACTIF' if test_mode else 'INACTIF'}, Tentative {tentative_num}")
    
    def set_contexte_projet(self, projet, langage):
        """Définit le contexte du projet pour l'apprentissage"""
        self.projet_courant = projet
        self.langage_courant = langage
    
    
    SYSTEM_PROMPT = """Tu es un expert polyvalent en développement logiciel. Génère du code CONCIS et EFFICACE dans le langage demandé.

Règles CRITIQUES:
1. Utilise la syntaxe EXACTE et CORRECTE pour le langage spécifié
2. Code COMPLET, COMPILABLE/EXÉCUTABLE immédiatement
3. Respecter les conventions et idiomes du langage
4. Inclure la gestion d'erreurs appropriée
5. Éviter les erreurs courantes détectées précédemment
6. Optimiser pour le langage spécifique

ERREURS À ÉVITER (basé sur l'apprentissage):
- Variables non définies
- Erreurs de type (ex: string + int)
- Imports manquants
- Parenthèses non fermées
- Mauvais opérateurs (= au lieu de ==)
- Syntaxe incorrecte spécifique au langage

FORMAT DE RÉPONSE:
- UNIQUEMENT le code source
- Pas d'explications, pas de markdown sauf si nécessaire
- Bonne indentation selon le langage
- Nom de fichier respecté"""

    def generer_code_adapte(self, demande, fichier_info, analyse, chemin_projet, introduire_bugs=False):
        """Génère du code adapté avec apprentissage"""
        nom_fichier = fichier_info['nom']
        print(f"      📝 Génération pour: {nom_fichier}")
        
       
        langage = self._detecter_langage_fichier(nom_fichier, analyse)
        self.langage_courant = langage
        
       
        stats = self.memoire.get_statistiques()
        cache_key = hashlib.md5(
            f"{demande}_{nom_fichier}_{self.tentative_num}_{stats.get('total_corrections', 0)}".encode()
        ).hexdigest()
        
        
        cached = self.cache.get(cache_key)
        if cached and not self.test_mode and self.tentative_num > 1:
            
            code_cached = cached.get('code', '')
            code_corrige, _ = self._appliquer_corrections_apprises(code_cached, langage, nom_fichier)
            return code_corrige
        
       
        try:
            prompt = self._creer_prompt_avec_apprentissage(demande, fichier_info, analyse, langage)
            
            
            temperature = 0.7 + (0.1 * self.tentative_num if self.test_mode else 0)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            
            code = response.choices[0].message.content
            code = self._nettoyer_code(code, langage)
            
           
            code_corrige_prealable, corrections_appliquees = self._appliquer_corrections_apprises(
                code, langage, nom_fichier
            )
            
            if corrections_appliquees:
                print(f"       {len(corrections_appliquees)} corrections apprises appliquées")
                for correction in corrections_appliquees[:2]:  # Afficher seulement 2
                    print(f"        → Évité: {correction.get('type', 'inconnu')}")
            
           
            bugs_introduits = []
            code_final = code_corrige_prealable
            
            if introduire_bugs and self.test_mode and self.tentative_num < 4:
              
                max_bugs = max(1, 3 - len(corrections_appliquees))
                code_final, bugs_introduits = self._introduire_bugs_intelligents(
                    code_corrige_prealable, langage, max_bugs
                )
            
          
            self._analyser_code_pour_apprentissage(code_final, langage, nom_fichier)
            
          
            self.cache.set(cache_key, {
                'nom_fichier': nom_fichier,
                'code': code_final,
                'langage': langage,
                'bugs_introduits': bugs_introduits,
                'corrections_appliquees': [c.get('type', '') for c in corrections_appliquees],
                'timestamp': time.time(),
                'tentative': self.tentative_num
            })
            
            return code_final
            
        except Exception as e:
            print(f"    Erreur génération: {str(e)[:50]}")
            code_secours = self._code_de_secours_simple(nom_fichier, demande, analyse, langage)
            
           
            code_corrige, _ = self._appliquer_corrections_apprises(code_secours, langage, nom_fichier)
            return code_corrige
    
    def _appliquer_corrections_apprises(self, code, langage, nom_fichier):
        """Applique les corrections apprises au code"""
        if not code:
            return code, []
        
      
        code_corrige, corrections_appliquees = self.correcteur.corriger_code(
            code=code,
            langage=langage,
            fichier=nom_fichier,
            tentative=self.tentative_num,
            projet=self.projet_courant
        )
        
       
        code_corrige = self.memoire.appliquer_corrections_connues(code_corrige, langage, nom_fichier)
        
        return code_corrige, corrections_appliquees
    
    def _analyser_code_pour_apprentissage(self, code, langage, nom_fichier):
        """Analyse le code pour détecter des patterns à apprendre"""
        if not code or self.tentative_num >= 4: 
            return
        
       
        erreurs_detectees = self._detecter_patterns_erreurs(code, langage, nom_fichier)
        
        for erreur in erreurs_detectees:
           
            erreur["langage"] = langage
            erreur["fichier"] = nom_fichier
            erreur["tentative"] = self.tentative_num
            erreur["projet"] = self.projet_courant
            
          
            erreur_id = self.memoire.enregistrer_erreur(erreur)
            
           
            self.erreurs_apprises.append({
                "id": erreur_id,
                "type": erreur.get("type"),
                "message": erreur.get("message", "")[:50],
                "langage": langage
            })
    
    def _detecter_patterns_erreurs(self, code, langage, nom_fichier):
        """Détecte des patterns d'erreurs courants dans le code"""
        erreurs = []
        lignes = code.split('\n')
        
        for i, ligne in enumerate(lignes, 1):
           
            if langage == "go":
                erreur = self._detecter_erreur_go(ligne, i, nom_fichier)
                if erreur:
                    erreurs.append(erreur)
            
            elif langage == "python":
                erreur = self._detecter_erreur_python(ligne, i, nom_fichier)
                if erreur:
                    erreurs.append(erreur)
            
            elif langage in ["javascript", "typescript"]:
                erreur = self._detecter_erreur_javascript(ligne, i, nom_fichier)
                if erreur:
                    erreurs.append(erreur)
        
        return erreurs
    
    def _detecter_erreur_go(self, ligne, num_ligne, nom_fichier):
        """Détecte les erreurs courantes en Go"""
        ligne_lower = ligne.lower()
        
        if 'undefinedvar' in ligne_lower or 'unusedvar' in ligne_lower:
            return {
                "type": "undefined_variable",
                "message": f"Variable potentiellement non définie ligne {num_ligne}",
                "ligne": num_ligne,
                "code_avant": ligne.strip(),
                "code_apres": f"// {ligne.strip()}  // Variable à vérifier",
                "severite": "warning"
            }
        
        if 'fmt.println("erreur' in ligne_lower and '" #' in ligne:
            return {
                "type": "syntax_error",
                "message": f"Parenthèse potentiellement manquante ligne {num_ligne}",
                "ligne": num_ligne,
                "code_avant": ligne.strip(),
                "code_apres": ligne.strip().replace('" #', '")  #'),
                "severite": "error"
            }
        
        return None
    
    def _detecter_erreur_python(self, ligne, num_ligne, nom_fichier):
        """Détecte les erreurs courantes en Python"""
        if 'variable_non_definie_' in ligne or 'undefined_var' in ligne:
            return {
                "type": "undefined_variable",
                "message": f"Variable potentiellement non définie ligne {num_ligne}",
                "ligne": num_ligne,
                "code_avant": ligne.strip(),
                "code_apres": f"# {ligne.strip()}  # Variable à vérifier",
                "severite": "warning"
            }
        
        return None
    
    def _detecter_erreur_javascript(self, ligne, num_ligne, nom_fichier):
        """Détecte les erreurs courantes en JavaScript/TypeScript"""
        if 'undefinedvariable_' in ligne or 'nondefinedvar' in ligne.lower():
            return {
                "type": "undefined_variable",
                "message": f"Variable potentiellement non définie ligne {num_ligne}",
                "ligne": num_ligne,
                "code_avant": ligne.strip(),
                "code_apres": f"// {ligne.strip()}  // Variable à vérifier",
                "severite": "warning"
            }
        
        return None
    
    def _introduire_bugs_intelligents(self, code, langage, max_bugs=3):
        """Introduit des bugs délibérés de manière intelligente"""
        if not self.test_mode or self.tentative_num >= 4:
            return code, []
        
        bugs_introduits = []
        code_avec_bugs = code
        
      
        bugs_possibles = self._get_bugs_prioritaires(langage)
        
       
        num_bugs = min(max_bugs, len(bugs_possibles))
        selected_bugs = random.sample(bugs_possibles, num_bugs)
        
        for bug_type in selected_bugs:
            code_avec_bugs, bug_applied = self._appliquer_bug_intelligent(bug_type, code_avec_bugs, langage)
            if bug_applied:
                bugs_introduits.append(bug_type)
              
                self._enregistrer_bug_pour_apprentissage(bug_type, langage)
        
        return code_avec_bugs, bugs_introduits
    
    def _get_bugs_prioritaires(self, langage):
        """Retourne les types de bugs à introduire selon le langage et l'apprentissage"""
       
        bugs_base = [
            'undefined_variable',
            'syntax_error',
            'missing_parenthesis'
        ]
        
      
        if langage == "go":
            bugs_specifiques = [
                'type_error_go',
                'wrong_assignment_go',
                'missing_import_go',
                'unused_variable_go'
            ]
        elif langage == "python":
            bugs_specifiques = [
                'indentation_error',
                'type_error_python',
                'name_error',
                'missing_import_python'
            ]
        elif langage in ["javascript", "typescript"]:
            bugs_specifiques = [
                'reference_error',
                'type_error_js',
                'undefined_variable_js',
                'missing_semicolon'
            ]
        else:
            bugs_specifiques = []
        
       
        tous_bugs = bugs_base + bugs_specifiques
        
        
        stats = self.memoire.get_statistiques()
        if stats.get('total_corrections', 0) > 0:
           
            return random.sample(tous_bugs, min(4, len(tous_bugs)))
        else:
        
            return bugs_base[:3]
    
    def _appliquer_bug_intelligent(self, bug_type, code, langage):
        """Applique un bug spécifique au code de manière intelligente"""
        if not code or len(code.strip()) < 10:
            return code, False
        
        lines = code.split('\n')
        bug_applied = False
        
        try:
            if bug_type == 'undefined_variable':
              
                if len(lines) > 3:
                    line_idx = random.randint(1, len(lines)-2)
                    if langage == "go":
                        lines.insert(line_idx, f"  undefinedVar{self.tentative_num} := \"test_bug\"")
                    elif langage == "python":
                        lines.insert(line_idx, f"  undefined_var_{self.tentative_num} = None")
                    elif langage in ["javascript", "typescript"]:
                        lines.insert(line_idx, f"  const undefinedVar{self.tentative_num} = undefined;")
                    bug_applied = True
            
            elif bug_type == 'type_error_go':
             
                if len(lines) > 3:
                    line_idx = random.randint(1, len(lines)-2)
                    lines.insert(line_idx, "  var x int = \"texte\"  // Erreur de type (bug)")
                    bug_applied = True
            
            elif bug_type == 'wrong_assignment_go':
                
                if len(lines) > 3:
                    line_idx = random.randint(1, len(lines)-2)
                    lines.insert(line_idx, "  x =: 5  // Mauvais opérateur (bug)")
                    bug_applied = True
            
            elif bug_type == 'missing_import_go':
              
                if "import (" in code:
                    for i, line in enumerate(lines):
                        if "import (" in line:
                            insert_pos = i + 1
                            lines.insert(insert_pos, f'    "inexistant/package{self.tentative_num}"  // Import bug')
                            break
                bug_applied = True
            
            elif bug_type == 'syntax_error':
               
                if len(lines) > 3:
                    line_idx = random.randint(1, len(lines)-2)
                    if langage == "go":
                        lines.insert(line_idx, f"  fmt.Println(\"Erreur tentative {self.tentative_num}\"  // Parenthèse manquante (bug)")
                    elif langage == "python":
                        lines.insert(line_idx, f"  print('Erreur tentative {self.tentative_num}'  # Guillemet manquant (bug)")
                    elif langage in ["javascript", "typescript"]:
                        lines.insert(line_idx, f"  console.log('Erreur tentative {self.tentative_num}'  // Parenthèse manquante (bug)")
                    bug_applied = True
            
            elif bug_type == 'missing_parenthesis':
                
                if len(lines) > 3:
                    line_idx = random.randint(1, len(lines)-2)
                    line = lines[line_idx]
                    if '(' in line and ')' in line:
                     
                        lines[line_idx] = line.rstrip(')') + "  // Parenthèse manquante (bug)"
                        bug_applied = True
            
            return '\n'.join(lines), bug_applied
            
        except Exception:
            return code, False
    
    def _enregistrer_bug_pour_apprentissage(self, bug_type, langage):
        """Enregistre un bug introduit pour l'apprentissage"""
        bug_info = {
            "type": bug_type,
            "langage": langage,
            "tentative": self.tentative_num,
            "projet": self.projet_courant,
            "timestamp": time.time(),
            "message": f"Bug délibéré introduit: {bug_type}",
            "corrige": False
        }
        
        self.memoire.enregistrer_erreur(bug_info)
    
    def _creer_prompt_avec_apprentissage(self, demande, fichier_info, analyse, langage):
        """Crée un prompt avec informations d'apprentissage"""
        nom_fichier = fichier_info["nom"]
        type_app = analyse.get('type_application', 'web')
        fonctionnalites = analyse.get('fonctionnalites_cles', [])
        
        
        erreurs_apprises = self._get_erreurs_apprises_pour_langage(langage)
        
      
        prompt = f"""
Génère le code complet pour ce fichier: {nom_fichier}

LANGAGE: {langage.upper()}
TYPE D'APPLICATION: {type_app}
FONCTIONNALITÉS: {', '.join(fonctionnalites)}
DEMANDE ORIGINALE: {demande}

ERREURS COURANTES À ÉVITER (basé sur apprentissage):
"""
        
       
        if erreurs_apprises:
            for i, erreur in enumerate(erreurs_apprises[:3], 1):
                prompt += f"{i}. {erreur}\n"
        else:
            prompt += "Aucune erreur spécifique apprise pour ce langage.\n"
        
        prompt += f"""
INSTRUCTIONS SPÉCIFIQUES POUR {langage.upper()}:
"""
        
       
        if langage == "go":
            prompt += """1. Utiliser la syntaxe Go correcte avec point-virgule optionnel
2. Respecter les conventions de nommage (camelCase)
3. Gestion d'erreurs avec retour multiple
4. Imports organisés en sections
5. Éviter les variables non utilisées (go vet)"""
        elif langage == "python":
            prompt += """1. Respecter PEP 8 (indentation 4 espaces)
2. Utiliser les docstrings
3. Gestion d'exceptions avec try/except
4. Éviter les variables globales
5. Type hints si Python 3.6+"""
        elif langage in ["javascript", "typescript"]:
            prompt += """1. Utiliser const/let au lieu de var
2. Points-virgules cohérents
3. Fonctions fléchées quand approprié
4. Gestion des promesses async/await
5. Éviter les variables non définies"""
        
        prompt += f"""

CRITÈRES DE QUALITÉ:
1. Code complet et fonctionnel
2. Respecter les bonnes pratiques du langage
3. Gestion d'erreurs appropriée incluse
4. Code prêt à être utilisé/compilé/exécuté immédiatement
5. Éviter les erreurs courantes listées ci-dessus

Retourne uniquement le code, sans explications.
"""
        
        return prompt
    
    def _get_erreurs_apprises_pour_langage(self, langage):
        """Retourne les erreurs apprises pour un langage spécifique"""
        erreurs = []
        
     
        stats = self.memoire.get_statistiques()
        total_corrections = stats.get('total_corrections', 0)
        
        if total_corrections > 0:
            if langage == "go":
                erreurs = [
                    "Variables non définies (undefinedVarX)",
                    "Erreurs de type (string dans int)",
                    "Parenthèses manquantes dans fmt.Println",
                    "Imports inexistants",
                    "Mauvais opérateur d'affectation (=: au lieu de :=)"
                ]
            elif langage == "python":
                erreurs = [
                    "Variables non définies",
                    "Indentation incorrecte",
                    "Imports manquants",
                    "Guillemets non fermés",
                    "Mauvais opérateur (= au lieu de ==)"
                ]
        
        return erreurs[:3] 
    
    def _detecter_langage_fichier(self, nom_fichier, analyse):
        """Détecte le langage d'un fichier simplement"""
        extension = nom_fichier.split('.')[-1].lower() if '.' in nom_fichier else ''
       
        if extension == 'go':
            return 'go'
        elif extension in ['js', 'jsx']:
            return 'javascript'
        elif extension in ['ts', 'tsx']:
            return 'typescript'
        elif extension == 'rs':
            return 'rust'
        elif extension == 'py':
            return 'python'
        elif extension == 'java':
            return 'java'
        elif extension in ['cpp', 'cc', 'cxx', 'h', 'hpp', 'hh', 'hxx']:
            return 'c++'
        elif extension == 'c':
            return 'c'
        elif extension == 'cs':
            return 'c#'
        elif extension == 'php':
            return 'php'
        elif extension == 'rb':
            return 'ruby'
        elif extension == 'swift':
            return 'swift'
        elif extension == 'kt' or extension == 'kts':
            return 'kotlin'
        elif extension == 'scala':
            return 'scala'
        elif extension == 'r':
            return 'r'
        elif extension == 'jl':
            return 'julia'
        elif extension == 'dart':
            return 'dart'
        elif extension == 'lua':
            return 'lua'
        elif extension == 'pl':
            return 'prolog'
        elif extension == 'hs':
            return 'haskell'
        elif extension == 'erl':
            return 'erlang'
        elif extension == 'ex' or extension == 'exs':
            return 'elixir'
        elif extension == 'clj' or extension == 'cljs':
            return 'clojure'
        elif extension == 'fs' or extension == 'fsx':
            return 'f#'
        elif extension == 'm' or extension == 'mm':
            return 'objective-c'
        elif extension == 'vue':
            return 'vue'
        elif extension == 'svelte':
            return 'svelte'
        elif extension == 'elm':
            return 'elm'
        elif extension == 'zig':
            return 'zig'
        elif extension == 'nim':
            return 'nim'
        elif extension == 'v':
            return 'v'
        elif extension == 'cr':
            return 'crystal'
        elif extension == 'groovy':
            return 'groovy'
        
       
        elif extension == 'sh' or extension == 'bash' or nom_fichier.startswith('.bash'):
            return 'bash'
        elif extension == 'ps1':
            return 'powershell'
        elif extension == 'bat' or extension == 'cmd':
            return 'batch'
        elif extension == 'fish':
            return 'fish'
        
      
        elif extension in ['html', 'htm']:
            return 'html'
        elif extension == 'css':
            return 'css'
        elif extension == 'scss' or extension == 'sass':
            return 'scss'
        elif extension == 'less':
            return 'less'
        
        
        elif extension == 'sql':
            return 'sql'
        elif extension == 'json':
            return 'json'
        elif extension == 'xml':
            return 'xml'
        elif extension == 'yaml' or extension == 'yml':
            return 'yaml'
        elif extension == 'toml':
            return 'toml'
        elif extension == 'ini':
            return 'ini'
        elif extension == 'env' or nom_fichier == '.env':
            return 'dotenv'
        
        
        elif extension == 'dockerfile' or nom_fichier == 'Dockerfile':
            return 'dockerfile'
        elif extension == 'tf' or extension == 'tfvars':
            return 'terraform'
        
        
        elif extension == 'md' or extension == 'markdown':
            return 'markdown'
        elif extension == 'tex':
            return 'latex'
        elif extension == 'rst':
            return 'restructuredtext'
        
        else:
            
            if nom_fichier == 'Makefile' or nom_fichier == 'makefile':
                return 'makefile'
            elif nom_fichier == 'CMakeLists.txt':
                return 'cmake'
            elif nom_fichier == 'package.json':
                return 'json'
            elif nom_fichier == 'Cargo.toml':
                return 'toml'
            elif nom_fichier == 'pyproject.toml':
                return 'toml'
            elif nom_fichier == 'go.mod':
                return 'gomod'
            elif nom_fichier == 'requirements.txt':
                return 'requirements'
            elif nom_fichier == 'composer.json':
                return 'json'
            elif nom_fichier == 'Gemfile':
                return 'ruby'
            elif nom_fichier == 'pom.xml':
                return 'xml'
            elif nom_fichier == 'build.gradle' or nom_fichier == 'build.gradle.kts':
                return 'groovy'
            
            return analyse.get('langage_principal', 'python')

    def _nettoyer_code(self, code, langage):
        """Nettoie le code généré simplement"""
     
        if '```' in code:
            parts = code.split('```')
            if len(parts) >= 3:
                
                code = parts[1].strip()
        
      
        phrases = [
            "Voici le code pour",
            "Here is the code for",
            "Code généré :",
            "Generated code:",
            f"Voici le fichier {langage}:",
            f"Here is the {langage} file:"
        ]
        
        for phrase in phrases:
            if code.startswith(phrase):
                code = code[len(phrase):].strip()
        
     
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        
        if code and not code.endswith('\n'):
            code += '\n'
        
        return code

    def _code_de_secours_simple(self, nom_fichier, demande, analyse, langage):
        """Code de secours ultra simple"""
        print(f"     Code de secours pour {nom_fichier}")
        
        
        type_app = analyse.get('type_application', 'app')
        fonctionnalites = analyse.get('fonctionnalites_cles', ['Application fonctionnelle'])
        
       
        if langage == 'go':
            return f'''// {nom_fichier}
// Application Go générée automatiquement
// Demande: {demande}

package main

import "fmt"

func main() {{
    fmt.Println("Application Go générée automatiquement")
    fmt.Printf("Type: %s\\n", "{type_app}")
    fmt.Println("Fonctionnalités:")
    for _, f := range {json.dumps(fonctionnalites)} {{
        fmt.Printf("  - %s\\n", f)
    }}
}}
'''
        
        elif langage == 'python':
            return f'''# {nom_fichier}
# Application Python générée automatiquement
# Demande: {demande}

def main():
    print("Application Python générée automatiquement")
    print(f"Type: {{type_app}}")
    print("Fonctionnalités:")
    for f in {json.dumps(fonctionnalites)}:
        print(f"  - {{f}}")

if __name__ == "__main__":
    main()
'''
        
        elif langage == 'javascript':
            return f'''// {nom_fichier}
// Application JavaScript générée automatiquement
// Demande: {demande}

console.log("Application JavaScript générée automatiquement");
console.log(`Type: {type_app}`);
console.log("Fonctionnalités:");
{json.dumps(fonctionnalites)}.forEach(f => {{
    console.log(`  - ${{f}}`);
}});
'''
        
        elif langage == 'typescript':
            return f'''// {nom_fichier}
// Application TypeScript générée automatiquement
// Demande: {demande}

console.log("Application TypeScript générée automatiquement");
console.log(`Type: {type_app}`);
console.log("Fonctionnalités:");
{json.dumps(fonctionnalites)}.forEach((f: string) => {{
    console.log(`  - ${{f}}`);
}});
'''
        
        elif langage == 'rust':
            return f'''// {nom_fichier}
// Application Rust générée automatiquement
// Demande: {demande}

fn main() {{
    println!("Application Rust générée automatiquement");
    println!("Type: {{}}", "{type_app}");
    println!("Fonctionnalités:");
    for f in {json.dumps(fonctionnalites)} {{
        println!("  - {{}}", f);
    }}
}}
'''
        
        elif langage == 'java':
            features_str = ""
            for feature in fonctionnalites:
                features_str += f'        System.out.println("  - {feature}");\n'
            
            return f'''// {nom_fichier}
// Application Java générée automatiquement
// Demande: {demande}

public class Main {{
    public static void main(String[] args) {{
        System.out.println("Application Java générée automatiquement");
        System.out.println("Type: {type_app}");
        System.out.println("Fonctionnalités:");
{features_str}
    }}
}}
'''
        
        elif langage == 'c++':
            return f'''// {nom_fichier}
// Application C++ générée automatiquement
// Demande: {demande}

#include <iostream>

int main() {{
    std::cout << "Application C++ générée automatiquement" << std::endl;
    std::cout << "Type: {type_app}" << std::endl;
    std::cout << "Fonctionnalités:" << std::endl;
    {json.dumps(fonctionnalites, ensure_ascii=False)}
    
    return 0;
}}
'''
        
        elif langage == 'html':
            features_html = ""
            for feature in fonctionnalites:
                features_html += f'        <li>{feature}</li>\n'
            
            return f'''<!DOCTYPE html>
<html>
<head>
    <title>Application générée</title>
</head>
<body>
    <h1>Application générée automatiquement</h1>
    <p>Demande: {demande}</p>
    <p>Type: {type_app}</p>
    <h2>Fonctionnalités:</h2>
    <ul>
{features_html}    </ul>
</body>
</html>'''
        
        elif nom_fichier == 'go.mod':
            return f'''module {analyse.get('nom_projet', 'myapp')}

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
)
'''
        
        elif nom_fichier == 'package.json':
            return f'''{{
  "name": "{analyse.get('nom_projet', 'myapp')}",
  "version": "1.0.0",
  "description": "{demande[:100]}",
  "main": "index.js",
  "scripts": {{
    "start": "node index.js"
  }},
  "dependencies": {{
    "express": "^4.18.2"
  }}
}}
'''
        
        elif nom_fichier == 'requirements.txt':
            deps = analyse.get('dependances', ['Flask'])
            return '\n'.join(deps) + '\n'
        
        elif nom_fichier == 'README.md':
            return f'''# {analyse.get('nom_projet', 'Application générée')}

## Description
{demande}

## Type
{type_app}

## Langage
{langage.upper()}

## Fonctionnalités
{chr(10).join(f'- {f}' for f in fonctionnalites)}

## Installation
Voir les instructions spécifiques au langage.

Généré automatiquement par AutoCoder.
'''
        
        elif nom_fichier == '.gitignore':
            if langage == 'go':
                return '''# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool, specifically when used with LiteIDE
*.out

# Dependency directories (remove the comment below to include it)
# vendor/
'''
            elif langage == 'python':
                return '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Virtual environments
venv/
env/
'''
            elif langage == 'javascript' or langage == 'typescript':
                return '''# Dependencies
node_modules/
npm-debug.log*

# Build
dist/
build/
'''
            else:
                return f'''# Fichiers à ignorer pour {langage}
*.log
node_modules/
.env
'''
        
        else:
           
            return f'''// {nom_fichier}
// Généré automatiquement par AutoCoder
// Langage: {langage}
// Demande: {demande}
// Type: {type_app}

// Application générée automatiquement
// Fonctionnalités: {', '.join(fonctionnalites)}

// Code de base - à compléter selon les besoins
'''

    def get_statistiques_apprentissage(self):
        """Retourne les statistiques d'apprentissage"""
        stats = self.memoire.get_statistiques()
        return {
            "corrections_apprises": stats.get('total_corrections', 0),
            "erreurs_detectees": len(self.erreurs_apprises),
            "langage_courant": self.langage_courant
        }



if __name__ == "__main__":
    print(" Test du rédacteur avec apprentissage...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    redacteur = RedacteurCode()
    
    
    analyse_go = {
        "langage_principal": "go",
        "type_application": "api",
        "fonctionnalites_cles": ["API REST", "JWT auth", "PostgreSQL"],
        "dependances": [],
        "nom_projet": "test_api"
    }
    
    fichier_info = {"nom": "main.go", "description": "Point d'entrée"}
    demande = "API REST en Go avec Gin"
    
   
    redacteur.set_contexte_projet("test_api", "go")
    redacteur.set_test_mode(True, 1)
    
    print(f"\nTest Go: {demande}")
    code = redacteur.generer_code_adapte(demande, fichier_info, analyse_go, "/test", True)
    
    print(f"\nCode généré (premières 10 lignes):")
    for i, line in enumerate(code.split('\n')[:10]):
        print(f"{i+1:3}: {line}")
    
    # Afficher les statistiques d'apprentissage
    stats = redacteur.get_statistiques_apprentissage()
    print(f"\n Statistiques apprentissage: {stats}")