# agents/architect_agent.py
import json
import re

class ArchitectAgent:
    """Agent qui conçoit l'architecture des solutions."""
    
    
    def __init__(self, llm_client=None):  # <-- Rend le paramètre optionnel
        if llm_client:
            self.client = llm_client
        else:
            # Créer un client par défaut si non fourni
            from utils.llm_client import LLMClient
            self.client = LLMClient(provider="groq")
    def design_solution(self, objective: str) -> dict:
        """
        Analyse l'objectif et conçoit l'architecture de la solution.
        
        Returns:
            {
                "language": "python|javascript|java|...",
                "framework": "flask|react|vue|...",
                "components": ["class1", "function1", ...],
                "files_needed": ["main.py", "utils.py", "test.py"],
                "dependencies": ["package1", "package2"],
                "architecture": "description de l'architecture"
            }
        """
        print("🏗️  ArchitectAgent: Analyse de l'objectif...")
        
        # 1. Détection du langage
        language = self._detect_language(objective)
        
        # 2. Conception de l'architecture
        system_prompt = """
        Tu es un architecte logiciel senior. 
        Analyse les besoins et conçois l'architecture technique.
        
        Réponds UNIQUEMENT en JSON avec cette structure:
        {
            "language": "langage principal",
            "framework": "framework si applicable",
            "components": ["liste des composants principaux"],
            "files_needed": ["liste des fichiers nécessaires"],
            "dependencies": ["dépendances à installer"],
            "architecture": "description textuelle de l'architecture",
            "entry_point": "fichier d'entrée principal"
        }
        """
        
        user_prompt = f"""
        OBJECTIF À RÉALISER: {objective}
        
        TÂCHES:
        1. Identifier le meilleur langage et framework
        2. Lister les composants logiciels nécessaires
        3. Déterminer les fichiers à créer
        4. Identifier les dépendances externes
        5. Décrire l'architecture globale
        
        POUR LES TESTS: Toujours inclure un fichier de tests
        """
        
        try:
            response = self.client.generate(system_prompt, user_prompt)
            
            # Nettoyer et parser la réponse JSON
            cleaned_response = self._extract_json(response)
            design = json.loads(cleaned_response)
            
            # S'assurer que le langage est cohérent
            if "language" not in design or not design["language"]:
                design["language"] = language
            
            print(f"   ✓ Architecture conçue: {design['language']} - {len(design['components'])} composants")
            return design
            
        except Exception as e:
            print(f"   ⚠️  Erreur de conception: {e}")
            # Fallback design
            return {
                "language": language,
                "framework": "standard",
                "components": ["MainClass", "UtilityFunctions"],
                "files_needed": ["solution.py", "utils.py", "test_solution.py"],
                "dependencies": [],
                "architecture": f"Solution simple en {language} pour: {objective}",
                "entry_point": "solution.py"
            }
    
    def _detect_language(self, objective: str) -> str:
        """Détecte le langage de programmation à partir de l'objectif."""
        system_prompt = "Tu es un expert en technologies. Identifie le langage de programmation."
        
        user_prompt = f"""
        Analyse cette demande et réponds par UN SEUL MOT:
        "python", "javascript", "java", "c", "cpp", "php", ou "ruby"
        
        Demande: {objective}
        
        Réponds seulement par le nom du langage.
        """
        
        try:
            response = self.client.generate(system_prompt, user_prompt).strip().lower()
            
            # Mapping des réponses
            lang_map = {
                "python": "python",
                "javascript": "javascript", "js": "javascript", "node": "javascript",
                "java": "java",
                "c": "c",
                "c++": "cpp", "cpp": "cpp",
                "php": "php",
                "ruby": "ruby",
                "html": "html",
                "css": "css"
            }
            
            # Chercher le langage dans la réponse
            for key, value in lang_map.items():
                if key in response:
                    return value
            
            # Défaut à Python
            return "python"
            
        except:
            return "python"
    
    def _extract_json(self, text: str) -> str:
        """Extrait le JSON d'une réponse texte."""
        # Chercher du JSON entre accolades
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        # Si pas trouvé, retourner un JSON par défaut
        return '{"language": "python", "components": [], "files_needed": ["solution.py"]}'
    
    def create_file_structure(self, design: dict, base_dir: str = "generated_code") -> list:
        """Crée la structure de fichiers basée sur le design."""
        files = []
        
        for filename in design.get("files_needed", []):
            file_type = self._get_file_type(filename, design["language"])
            
            files.append({
                "path": f"{base_dir}/{filename}",
                "type": file_type,
                "purpose": self._get_file_purpose(filename),
                "is_test": "test" in filename.lower() or "spec" in filename.lower()
            })
        
        return files
    
    def _get_file_type(self, filename: str, language: str) -> str:
        """Détermine le type de fichier."""
        ext = filename.split('.')[-1].lower()
        
        type_map = {
            "py": "python",
            "js": "javascript", "jsx": "javascript", "ts": "typescript",
            "java": "java",
            "cpp": "cpp", "c": "c",
            "php": "php",
            "rb": "ruby",
            "html": "html",
            "css": "css",
            "json": "json",
            "md": "markdown",
            "txt": "text"
        }
        
        return type_map.get(ext, "unknown")
    
    def _get_file_purpose(self, filename: str) -> str:
        """Détermine l'objectif du fichier."""
        name = filename.lower()
        
        if "test" in name or "spec" in name:
            return "tests"
        elif "main" in name or "app" in name:
            return "entry_point"
        elif "util" in name:
            return "utilities"
        elif "config" in name or "settings" in name:
            return "configuration"
        else:
            return "implementation"