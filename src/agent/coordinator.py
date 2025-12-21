# agents/coordinator.py
# SUPPRIMER cette ligne: from ast import Assign
import json
import time
from pathlib import Path
from agent.architect_agent import ArchitectAgent
from agent.coder_agent import CoderAgent
from agent.debugger_agent import DebuggerAgent
from agent.tester_agent import TesterAgent
from utils.file_manager import write_code, read_code
from utils.llm_client import LLMClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Coordinator:
    """Agent qui orchestre tous les autres agents."""
    
    def __init__(self, provider="groq"):
        # Initialiser le client LLM
        self.llm_client = LLMClient(provider=provider)
        
        # Initialiser les agents
        self.architect = ArchitectAgent(self.llm_client)
        self.coder = CoderAgent(self.llm_client)
        self.tester = TesterAgent()  # Pas besoin de llm_client
        self.debugger = DebuggerAgent(self.llm_client)
        
        # Historique
        self.history = []  # Historique principal
        self.iteration_history = []  # Historique spécifique aux itérations
        self.current_iteration = 0
        self.current_objective = ""
        self.current_design = {}
        self.max_iterations = 3
        
    def solve_problem(self, objective: str, max_iterations: int = 3) -> dict:
        """
        Résout un problème en faisant collaborer tous les agents.
        
        Returns:
            {
                "status": "success|failure|partial",
                "iterations": nombre d'itérations,
                "final_code": "code final",
                "tests_passed": bool,
                "history": [...]
            }
        """
        self.current_objective = objective
        self.max_iterations = max_iterations
        self.current_iteration = 0
        
        print(f"\n{'='*60}")
        print(f"🎯 DÉBUT: {objective}")
        print(f"{'='*60}")
        
        # ITÉRATION 0: Conception
        print("\n📋 PHASE 1: CONCEPTION")
        print("-" * 40)
        
        self.current_design = self.architect.design_solution(objective)
        self.history.append({
            "iteration": self.current_iteration,
            "phase": "conception",
            "design": self.current_design  # <-- CORRECTION: utiliser self.current_design
        })
        
        print(f"   Langage: {self.current_design.get('language', 'python')}")
        print(f"   Composants: {len(self.current_design.get('components', []))}")
        print(f"   Fichiers: {len(self.current_design.get('files_needed', []))}")
        
        # Boucle d'amélioration
        for iteration in range(1, max_iterations + 1):
            self.current_iteration = iteration
            print(f"\n🔄 ITÉRATION {iteration}/{max_iterations}")
            print("-" * 40)
            
            result = self._run_iteration(iteration)
            
            if result["status"] == "success":
                print(f"\n{'🎉' * 20}")
                print(f"🎉 SUCCÈS à l'itération {iteration}")
                print(f"{'🎉' * 20}")
                return self._create_final_result("success", iteration)
        
        # Si on arrive ici, toutes les itérations ont échoué
        print(f"\n{'❌' * 20}")
        print("❌ ÉCHEC - Maximum d'itérations atteint")
        print(f"{'❌' * 20}")
        
        # Tentative finale avec revue complète
        final_attempt = self._final_review()
        return self._create_final_result("failure", max_iterations, final_attempt)
    
    def _run_iteration(self, iteration: int) -> dict:
        """Exécute une itération complète."""
        # Étape 1: Implémentation
        print("💻 Étape 1: Implémentation...")
        implementation = self.coder.implement_design(self.current_design)
        
        # Sauvegarder les fichiers
        for filename, code in implementation.get("files", {}).items():
            is_test = "test" in filename.lower()
            write_code(code, 
           is_test=is_test, 
           language=self.current_design.get("language", "python"), 
           filename=filename)  # <-- AJOUTEZ CE PARAMÈTRE
        # Enregistrer l'implémentation dans l'historique
        self.iteration_history.append({
            "iteration": iteration,
            "phase": "implementation",
            "files": list(implementation.get("files", {}).keys())
        })
        
        # Étape 2: Tests
        print("🧪 Étape 2: Tests...")
        test_success, test_summary, test_details = self.tester.run_tests(
            language=self.current_design.get("language", "python")
        )
        
        # Enregistrer les tests dans l'historique
        self.iteration_history.append({
            "iteration": iteration,
            "phase": "testing",
            "test_success": test_success,
            "test_summary": test_summary,
            "test_details_count": len(test_details)
        })
        
        if test_success:
            return {"status": "success", "details": test_details}
        
        # Étape 3: Analyse des erreurs
        print("🐛 Étape 3: Analyse des erreurs...")
        
        # Pour chaque test échoué, analyser et corriger
        debug_applied = False
        for test_result in test_details:
            if not test_result.get("passed", True):
                # Lire le code du fichier testé
                tested_file = test_result["file"].replace("test_", "").replace(".py", ".py")
                try:
                    current_code = read_code(is_test=False, language=self.current_design.get("language", "python"))
                except:
                    current_code = ""
                
                # Analyser l'erreur
                analysis = self.debugger.analyze_failure(
                    code=current_code,
                    error_output=test_result.get("error", "") + test_result.get("output", ""),
                    context={"iteration": iteration, "test_file": test_result["file"]}
                )
                
                # Générer la correction
                corrected_code = self.debugger.generate_fix(
                    code=current_code,
                    analysis=analysis,
                    language=self.current_design.get("language", "python")
                )
                
                # Sauvegarder la correction
                write_code(corrected_code, is_test=False, language=self.current_design.get("language", "python"))
                
                # Enregistrer dans l'historique
                self.iteration_history.append({
                    "iteration": iteration,
                    "phase": "debug",
                    "file": tested_file,
                    "error_type": analysis.get("error_type", "unknown"),
                    "correction_applied": True
                })
                
                debug_applied = True
        
        if debug_applied:
            return {"status": "retry", "details": test_details}
        else:
            return {"status": "failure", "details": test_details}
    
    def _final_review(self) -> str:
        """Tentative finale après échec de toutes les itérations."""
        print("\n🔍 REVUE FINALE: Analyse approfondie...")
        
        # Récupérer tout le code généré
        all_code = ""
        for item in self.iteration_history:
            if item.get("phase") == "implementation":
                # Essayer de lire les fichiers depuis le disque
                try:
                    code = read_code(is_test=False, language=self.current_design.get("language", "python"))
                    all_code += f"\n\n=== Code actuel ===\n{code[:1000]}"
                except:
                    pass
        
        # Demander une solution finale
        system_prompt = """
        Expert senior en résolution de problèmes.
        Fournissez une solution COMPLÈTE et TESTÉE.
        Répondez UNIQUEMENT avec le code final.
        """
        
        user_prompt = f"""
        PROBLÈME: {self.current_objective}
        
        TOUTES LES TENTATIVES ONT ÉCHOUÉ.
        
        HISTORIQUE DES TENTATIVES:
        {json.dumps(self.iteration_history[-3:], indent=2)}
        
        CODE GÉNÉRÉ (extraits):
        {all_code[:2000]}
        
        Fournissez une solution FINALE et ROBUSTE.
        """
        
        final_solution = self.llm_client.generate(system_prompt, user_prompt)
        return final_solution
    
    def _create_final_result(self, status: str, iterations: int, final_code: str = None) -> dict:
        """Crée le résultat final."""
        try:
            current_code = read_code(is_test=False, language=self.current_design.get("language", "python"))
        except:
            current_code = final_code or ""
        
        return {
            "status": status,
            "iterations": iterations,
            "final_code": current_code,
            "design": self.current_design,
            "history": self.iteration_history,  # <-- CORRECTION: self.iteration_history
            "timestamp": time.time()
        }
    
    def save_debug_info(self, filename: str = "debug_history.json"):
        """Sauvegarde l'historique de débogage."""
        debug_dir = Path("debug_history")
        debug_dir.mkdir(exist_ok=True)
        
        debug_data = {
            "objective": self.current_objective,
            "design": self.current_design,
            "history": self.iteration_history,  # <-- CORRECTION: self.iteration_history
            "timestamp": time.time()
        }
        
        with open(debug_dir / filename, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Historique sauvegardé: debug_history/{filename}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Test rapide
    coordinator = Coordinator()
    
    test_objective = "Créer une classe GestionnaireNotes avec méthodes ajouter_note, moyenne, et sauvegarde JSON"
    
    result = coordinator.solve_problem(test_objective, max_iterations=2)
    
    print(f"\n📊 RÉSULTAT: {result['status'].upper()}")
    print(f"   Itérations: {result['iterations']}")
    print(f"   Langage: {result['design'].get('language', 'python')}")