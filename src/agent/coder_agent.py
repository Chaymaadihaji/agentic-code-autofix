# agent/coder_agent.py
import os
import json
from utils.llm_client import LLMClient  # Assurez-vous d'avoir cette importation

class CoderAgent:
    """Agent qui génère le code d'implémentation."""
    
    def __init__(self, llm_client=None, provider="groq"):  # <-- MODIFIER
        # Si llm_client est fourni, l'utiliser
        if llm_client:
            self.llm_client = llm_client
            self.provider = llm_client.provider if hasattr(llm_client, 'provider') else "groq"
        else:
            # Sinon, en créer un nouveau
            self.llm_client = LLMClient(provider=provider)
            self.provider = provider
        
        self.generated_files = []
    
    def implement_design(self, design: dict) -> dict:
        """
        Implémente le design en générant le code.
        
        Returns:
            {
                "files": {"filename.py": "code...", ...},
                "language": "python",
                "status": "complete"
            }
        """
        print("💻 CoderAgent: Implémentation du design...")
        
        language = design.get("language", "python")
        components = design.get("components", [])
        files_needed = design.get("files_needed", [])
        
        files = {}
        
        # Générer le code pour chaque fichier
        for filename in files_needed:
            print(f"   📝 Création de: {filename}")
            try:
                # Générer le code avec le LLM
                code = self._generate_code_for_file(filename, design, language)
                
                if code:
                    files[filename] = code
                    self.generated_files.append(filename)
                    print(f"   ✓ Code généré pour {filename}")
                else:
                    print(f"   ❌ Échec de génération pour {filename}")
                    
            except Exception as e:
                print(f"   ❌ Erreur sur {filename}: {e}")
        
        print(f"   ✓ {len(files)} fichiers générés")
        
        return {
            "files": files,
            "language": language,
            "status": "complete" if files else "failed"
        }
    
    def _generate_code_for_file(self, filename: str, design: dict, language: str) -> str:
        """Génère le code pour un fichier spécifique."""
        
        system_prompt = f"""
        Expert en programmation {language}.
        Vous générez du code propre, documenté et testable.
        Répondez UNIQUEMENT avec le code source, sans explications supplémentaires.
        """
        
        user_prompt = f"""
        DESIGN:
        {json.dumps(design, indent=2)}
        
        FICHIER: {filename}
        
        Générez le code complet pour ce fichier.
        Incluez les imports nécessaires, la documentation et des exemples d'utilisation si approprié.
        """
        
        try:
            code = self.llm_client.generate(system_prompt, user_prompt)
            return code.strip()
        except Exception as e:
            print(f"      Erreur LLM: {e}")
            # Fallback: code de base
            return self._generate_fallback_code(filename, design, language)
    
    def _generate_fallback_code(self, filename: str, design: dict, language: str) -> str:
        """Génère un code de secours si le LLM échoue."""
        if language == "python":
            if "todo" in filename.lower():
                return '''"""
Module TodoList - Gestionnaire de tâches
"""

import json
from datetime import datetime

class Tache:
    """Représente une tâche."""
    
    def __init__(self, titre: str, description: str = ""):
        self.titre = titre
        self.description = description
        self.terminee = False
        self.date_creation = datetime.now()
        self.date_terminaison = None
    
    def terminer(self):
        """Marque la tâche comme terminée."""
        self.terminee = True
        self.date_terminaison = datetime.now()
    
    def to_dict(self):
        """Convertit la tâche en dictionnaire."""
        return {
            "titre": self.titre,
            "description": self.description,
            "terminee": self.terminee,
            "date_creation": self.date_creation.isoformat(),
            "date_terminaison": self.date_terminaison.isoformat() if self.date_terminaison else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crée une tâche depuis un dictionnaire."""
        tache = cls(data["titre"], data.get("description", ""))
        tache.terminee = data.get("terminee", False)
        # Note: les dates sont stockées comme strings
        return tache

class TodoList:
    """Gestionnaire de liste de tâches."""
    
    def __init__(self, nom: str = "Ma TodoList"):
        self.nom = nom
        self.taches = []
    
    def ajouter_tache(self, titre: str, description: str = ""):
        """Ajoute une nouvelle tâche."""
        nouvelle_tache = Tache(titre, description)
        self.taches.append(nouvelle_tache)
        return nouvelle_tache
    
    def terminer_tache(self, index: int):
        """Termine une tâche par son index."""
        if 0 <= index < len(self.taches):
            self.taches[index].terminer()
            return True
        return False
    
    def lister_taches(self, filtre_terminees: bool = None):
        """Liste les tâches avec option de filtrage."""
        if filtre_terminees is None:
            return self.taches
        
        return [t for t in self.taches if t.terminee == filtre_terminees]
    
    def sauvegarder_json(self, fichier: str = "todolist.json"):
        """Sauvegarde la todo list en JSON."""
        data = {
            "nom": self.nom,
            "taches": [tache.to_dict() for tache in self.taches]
        }
        
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def charger_json(cls, fichier: str = "todolist.json"):
        """Charge une todo list depuis JSON."""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            todolist = cls(data["nom"])
            todolist.taches = [Tache.from_dict(t) for t in data.get("taches", [])]
            return todolist
        except FileNotFoundError:
            return cls()
    
    def __str__(self):
        """Représentation textuelle."""
        result = [f"TodoList: {self.nom}", "=" * 30]
        for i, tache in enumerate(self.taches):
            status = "✓" if tache.terminee else "◯"
            result.append(f"{i}. [{status}] {tache.titre}")
        return "\n".join(result)

# Exemple d'utilisation
if __name__ == "__main__":
    # Création d'une todo list
    ma_liste = TodoList("Mes courses")
    
    # Ajout de tâches
    ma_liste.ajouter_tache("Acheter du lait", "2 litres")
    ma_liste.ajouter_tache("Acheter des œufs", "12 œufs")
    
    # Marquer une tâche comme terminée
    ma_liste.terminer_tache(0)
    
    # Lister les tâches
    print(ma_liste)
    
    # Sauvegarder
    ma_liste.sauvegarder_json()
    
    # Charger
    liste_chargee = TodoList.charger_json()
    print(liste_chargee)'''
        else:
            # Fallback générique
            return f"# Fichier: {filename}\n# Code pour {design.get('objective', 'projet')}\n\n# TODO: Implémenter le code"