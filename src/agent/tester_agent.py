# agents/tester_agent.py
import subprocess
import sys
import os
from pathlib import Path

class TesterAgent:
    """Agent qui écrit et exécute les tests."""
    
    def __init__(self, llm_client=None):  # <-- Accepter llm_client en option
        self.test_results = []
        self.llm_client = llm_client  # <-- Stocker si fourni
    def create_tests(self, design: dict, implementation: dict) -> dict:
        """
        Crée les fichiers de test appropriés.
        
        Returns:
            {
                "test_files": ["test_file1.py", ...],
                "test_strategy": "description",
                "coverage_goals": ["goal1", ...]
            }
        """
        print("🧪 TesterAgent: Planification des tests...")
        
        language = design.get("language", "python")
        components = design.get("components", [])
        
        test_plan = {
            "test_files": [],
            "test_strategy": f"Tests unitaires pour {len(components)} composants en {language}",
            "coverage_goals": [
                "Toutes les fonctions publiques",
                "Cas limites et erreurs",
                "Intégration basique"
            ]
        }
        
        # Générer les noms de fichiers de test
        for component in components:
            test_filename = f"test_{component.lower()}.py" if language == "python" else f"{component}Test.js"
            test_plan["test_files"].append(test_filename)
        
        # Ajouter un fichier de test principal
        if language == "python":
            test_plan["test_files"].append("test_main.py")
        
        print(f"   ✓ {len(test_plan['test_files'])} fichiers de test planifiés")
        return test_plan
    
    def run_tests(self, language: str = "python", test_dir: str = "tests") -> tuple:
        """
        Exécute les tests et retourne les résultats.
        
        Returns:
            (success: bool, output: str, details: list)
        """
        print("🧪 TesterAgent: Exécution des tests...")
        
        if language == "python":
            return self._run_python_tests(test_dir)
        elif language == "javascript":
            return self._run_javascript_tests(test_dir)
        else:
            return False, f"Langage non supporté: {language}", []
    
    def _run_python_tests(self, test_dir: str) -> tuple:
        """Exécute les tests Python avec unittest."""
        try:
            # Vérifier si le dossier de tests existe
            if not os.path.exists(test_dir):
                return False, f"Dossier de tests introuvable: {test_dir}", []
            
            # Trouver tous les fichiers de test
            test_files = []
            for file in Path(test_dir).glob("test_*.py"):
                test_files.append(str(file))
            
            if not test_files:
                return False, "Aucun fichier de test trouvé", []
            
            # Exécuter les tests
            all_results = []
            total_passed = 0
            total_failed = 0
            
            for test_file in test_files:
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", test_file, "-v"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Analyser les résultats
                passed = result.returncode == 0
                output = result.stdout
                
                if passed:
                    total_passed += 1
                else:
                    total_failed += 1
                
                all_results.append({
                    "file": Path(test_file).name,
                    "passed": passed,
                    "output": output[:1000],  # Limiter la taille
                    "error": result.stderr[:500] if result.stderr else ""
                })
            
            # Résumé global
            success = total_failed == 0
            summary = f"Tests Python: {total_passed} passés, {total_failed} échoués"
            
            return success, summary, all_results
            
        except subprocess.TimeoutExpired:
            return False, "Timeout: les tests ont pris trop de temps", []
        except Exception as e:
            return False, f"Erreur d'exécution: {str(e)}", []
    
    def _run_javascript_tests(self, test_dir: str) -> tuple:
        """Exécute les tests JavaScript (simulation)."""
        # Pour JavaScript, vous devriez installer Jest ou Mocha
        # Ici, simulation basique
        return True, "Tests JavaScript (simulation - installer Jest pour vrais tests)", []
    
    def analyze_test_results(self, results: list) -> dict:
        """Analyse les résultats de tests pour identifier les problèmes."""
        analysis = {
            "total_tests": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "failed": sum(1 for r in results if not r["passed"]),
            "common_errors": [],
            "suggestions": []
        }
        
        # Identifier les erreurs communes
        error_patterns = [
            ("ImportError", "Problème d'importation"),
            ("AssertionError", "Échec d'assertion"),
            ("AttributeError", "Attribut non trouvé"),
            ("TypeError", "Type incorrect"),
            ("NameError", "Variable non définie")
        ]
        
        for result in results:
            if not result["passed"]:
                for pattern, description in error_patterns:
                    if pattern in result.get("error", ""):
                        analysis["common_errors"].append(f"{description} dans {result['file']}")
        
        # Générer des suggestions
        if analysis["failed"] > 0:
            analysis["suggestions"].append("Vérifier les imports et les dépendances")
            analysis["suggestions"].append("Tester avec des valeurs limites")
        
        return analysis