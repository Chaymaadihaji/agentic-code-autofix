# src/agent/code_manager.py

import sys
from pathlib import Path
import time
import os

# --- CORRECTION DE L'IMPORTATION ---
current_file_path = Path(__file__).resolve()
src_dir = current_file_path.parent.parent
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))
# -----------------------------------------------------------------------

from utils.config_loader import load_config
from utils.file_manager import write_code, read_code

# Import conditionnel des clients LLM
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ Package 'groq' non installé. Exécutez: pip install groq")

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Package 'google-genai' non installé. Exécutez: pip install google-genai")

class CodeManager:
    """
    Gère la génération et la correction du code via différents fournisseurs LLM.
    """
    def __init__(self):
        """Initialise le client LLM selon la configuration."""
        self.config = load_config()
        self.provider = self.config['LLM_PROVIDER']
        self.model = self.config['LLM_MODEL']
        self.api_key = self.config['API_KEY']
        self.current_objective = None  # Pour stocker l'objectif courant
        
        # Initialiser le client selon le fournisseur
        if self.provider == "groq":
            if not GROQ_AVAILABLE:
                raise ImportError("Package 'groq' requis. Exécutez: pip install groq")
            self.client = Groq(api_key=self.api_key)
            print(f"✅ CodeManager initialisé. Fournisseur: Groq, Modèle: {self.model}")
            
        elif self.provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise ImportError("Package 'google-genai' requis. Exécutez: pip install google-genai")
            # Gemini utilise la variable d'environnement déjà définie
            self.client = genai.Client()
            print(f"✅ CodeManager initialisé. Fournisseur: Gemini, Modèle: {self.model}")
            
        elif self.provider == "openai":
            # Implémentez OpenAI si nécessaire
            raise NotImplementedError("Support OpenAI à implémenter")
            
        else:
            raise ValueError(f"Fournisseur non supporté: {self.provider}")

    def _generate_content(self, system_prompt: str, user_prompt: str) -> str:
        """Appelle l'API LLM avec un mécanisme de secours."""
        max_retries = 5
        retry_delay = 10
        
        for attempt in range(max_retries):
            try:
                if self.provider == "groq":
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                    
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=2000,
                        top_p=1,
                        stream=False
                    )
                    raw_text = response.choices[0].message.content
                    
                elif self.provider == "gemini":
                    config = types.GenerateContentConfig(system_instruction=system_prompt)
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=[user_prompt],
                        config=config,
                    )
                    raw_text = response.text
                
                # Nettoyage Markdown
                raw_text = raw_text.strip()
                if raw_text.startswith('```'):
                    lines = raw_text.splitlines()
                    if len(lines) > 2 and lines[0].startswith('```') and lines[-1] == '```':
                        raw_text = '\n'.join(lines[1:-1]).strip()
                
                return raw_text
                
            except Exception as e:
                error_str = str(e)
                
                # Logique de retry commune
                if "429" in error_str or "503" in error_str or "overloaded" in error_str.lower():
                    print(f"⚠️ Serveur surchargé (Tentative {attempt+1}/{max_retries}). Nouvel essai dans {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"❌ Erreur API {self.provider}: {e}")
                    raise e
        
        raise Exception(f"🚨 L'API {self.provider} est restée indisponible après plusieurs tentatives.")

    def generate_initial_solution(self, objective: str):
        """Génère le code selon le langage détecté ou Python par défaut."""
        self.current_objective = objective
        
        # 1. Étape de détection du langage
        detect_prompt = (
            f"Analyse l'objectif suivant : '{objective}'. "
            "De quel langage de programmation s'agit-il ? Réponds par un seul mot "
            "(ex: Python, C, Java, JavaScript, C++). Si aucun langage n'est mentionné, "
            "réponds 'Python' par défaut."
        )
        
        # On sauvegarde le langage dans self pour y accéder depuis main.py
        self.langage_cible = self._generate_content("Tu es un assistant technique précis.", detect_prompt).strip().lower().replace('.', '')
        
        print(f"\n--- 🚀 Langage détecté : {self.langage_cible.capitalize()} ---")

        # 2. Prompt système dynamique
        system_prompt = (
            f"Vous êtes un expert en développement {self.langage_cible}. "
            f"Générez du code {self.langage_cible} FONCTIONNEL. "
            f"Répondez UNIQUEMENT avec le code {self.langage_cible} sans explications."
        )

        # 3. Générer le Code Solution
        code_prompt = f"Générer la fonction/classe en {self.langage_cible} pour : {objective}"
        solution_code = self._generate_content(system_prompt, code_prompt)
        
        # ✅ IMPORTANT : On passe le langage à write_code
        write_code(solution_code, is_test=False, language=self.langage_cible)

        # 4. Générer les tests adaptés au langage
        test_prompt = f"""
        Générez des tests pour l'objectif : {objective}
        LANGAGE : {self.langage_cible}
        
        EXIGENCES CRITIQUES :
        1. Tu DOIS importer la classe ou la fonction depuis le fichier solution. 
         Exemple pour Python : "from generated_code.solution import GestionnaireNotes"
         2. Utilise EXACTEMENT les mêmes noms de variables.
          3. RÉPONDS UNIQUEMENT AVEC LE CODE DU TEST.
        """
        
        test_code = self._generate_content(system_prompt, test_prompt)
        # ✅ IMPORTANT : On passe aussi le langage ici
        write_code(test_code, is_test=True, language=self.langage_cible)
        
        print(f"✅ Solution et tests ({self.langage_cible}) générés avec succès.")

    def fix_solution(self, original_code: str, test_output: str) -> str:
        """Demande à l'IA de corriger le code en fonction de l'erreur."""
        print(f"\n--- 🧠 Réflexion et Correction ({self.langage_cible}) ---")

        # Récupérer le langage stocké (Python par défaut si absent)
        lang = getattr(self, 'langage_cible', 'python')

        try:
            test_code = read_code(is_test=True, language=lang)
        except:
            test_code = "Test non disponible"

        # On rend le prompt de correction dynamique aussi !
       # 2. Créer un prompt système détaillé et dynamique
        system_prompt = (
    f"Vous êtes un expert en {lang.upper()}.\n"
    f"MISSION : Réécrire le fichier SOLUTION COMPLET sans aucune omission.\n\n"
    f"RÈGLES CRITIQUES :\n"
    f"1. RÉPONDEZ UNIQUEMENT AVEC LE CODE COMPLET. Ne donnez pas juste la correction.\n"
    f"2. JAVASCRIPT : Vous DEVEZ inclure la fonction ET l'exportation.\n"
    f"   Exemple de structure attendue :\n"
    f"   function addition(a, b) {{ return a + b; }}\n"
    f"   module.exports = {{ addition }};\n"
    f"3. INTERDICTION : Ne mettez pas de balises ```, pas de texte, pas d'explications.\n"
    f"4. Gardez exactement les mêmes noms de fonctions que dans les tests."
    f"7. RIGOUREUX : En Python, les booléens sont des instances d'entiers. Si on demande des nombres, assurez-vous d'exclure explicitement les booléens avec type(x) is not bool pour éviter les erreurs de logique classiques"
)      
        user_prompt = f"LANGAGE: {lang}\nCODE SOURCE:\n{original_code}\n\nERREUR:\n{test_output}\n\nTEST:\n{test_code}"
        
        return self._generate_content(system_prompt, user_prompt)
    
    def final_review(self, objective: str, all_attempts: list, test_failures: list):
        """
        Demande à l'IA une revue complète après l'échec de toutes les tentatives.
        """
        print(f"\n--- 🎯 REVUE FINALE ({self.provider}) - Analyse des échecs ---")
        
        # 1. Construire l'historique des tentatives
        attempts_text = ""
        for i, (code, error) in enumerate(zip(all_attempts, test_failures)):
            attempts_text += f"\n{'='*60}\nTENTATIVE #{i+1}\n{'='*60}\n"
            attempts_text += f"CODE:\n```python\n{code}\n```\n\n"
            attempts_text += f"ERREUR:\n```\n{error}\n```\n"
        
        # 2. Lire le code de test actuel
        try:
            test_code = read_code(is_test=True)
        except:
            test_code = "Test non disponible"
        
        # 3. Prompt système pour la revue finale
        system_prompt = (
            "Vous êtes un architecte logiciel senior. Analysez pourquoi toutes les tentatives "
            "automatiques ont échoué et fournissez une solution ROBUSTE et ÉLÉGANTE.\n"
            "Votre réponse doit être du code Python PRÊT À L'EMPLOI, sans commentaires supplémentaires."
        )
        
        # 4. Prompt utilisateur détaillé
        user_prompt = (
            "## PROBLÈME À RÉSOUDRE (ÉCHEC MULTIPLE)\n"
            f"OBJECTIF: {objective}\n\n"
            
            "## HISTORIQUE COMPLET DES TENTATIVES ÉCHOUÉES"
            f"{attempts_text}\n\n"
            
            "## CODE DE TEST ACTUEL (ce que la solution doit passer)\n"
            f"```python\n{test_code}\n```\n\n"
            
            "## ANALYSE REQUISE\n"
            "1. Pourquoi les tentatives précédentes échouent-elles ?\n"
            "2. Y a-t-il un malentendu fondamental sur les exigences ?\n"
            "3. Quelle est la solution CORRECTE et COMPLÈTE ?\n\n"
            
            "## SOLUTION FINALE (code Python uniquement):"
        )
        
        # 5. Générer la solution finale
        final_solution = self._generate_content(system_prompt, user_prompt)
        
        # 6. Écrire la solution finale
        print(f"📝 Écriture de la solution finale...")
        write_code(final_solution, is_test=False)
        
        return final_solution

# --- Test rapide ---
if __name__ == '__main__':
    try:
        manager = CodeManager()
        test_objective = "Créer une fonction 'calculer_somme' qui prend une liste de nombres et retourne leur somme."
        
        manager.generate_initial_solution(test_objective)

        print("\n--- CODE SOLUTION (generated_code/solution.py) ---")
        print(read_code(is_test=False))
        print("\n--- CODE TEST (tests/test_generated_code.py) ---")
        print(read_code(is_test=True))
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}")