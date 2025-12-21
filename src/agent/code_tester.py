# src/agent/code_tester.py

import subprocess
import os
import unittest
import sys
from pathlib import Path

# Définition des chemins
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TESTS_DIR = BASE_DIR / "tests"
TEST_FILE = TESTS_DIR / "test_generated_code.py"

# --- CORRECTION DE L'IMPORTATION (POUR LES TESTS) ---
# Ceci ajoute le répertoire RACINE du projet ('agentic-code-autofix/')
# au chemin de recherche Python pour que l'import 'from generated_code.solution import ...'
# dans le fichier de test fonctionne correctement.
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))
# --------------------------------------------------


class CodeTester:
    """
    Exécute les tests unitaires et analyse les résultats pour l'Agent.
    """
   # Dans src/agent/code_tester.py

    def run_tests(self) -> tuple[bool, str]:
        if not TEST_FILE.exists():
            return False, "Erreur: Le fichier de test n'existe pas."

        try:
            # 1. Préparation de l'environnement (pour trouver les modules)
            env_vars = os.environ.copy()
            env_vars['PYTHONPATH'] = str(BASE_DIR) 

            # 2. Exécution du test avec le bon environnement
            result = subprocess.run(
                [sys.executable, str(TEST_FILE)],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR),
                env=env_vars,
                timeout=15
            )

            output = result.stdout + result.stderr
            
            # Vérification des erreurs dans la sortie de Pytest ou Unittest
            if "FAIL" in output or "ERROR" in output or result.returncode != 0:
                return False, output
            
            return True, output

        except Exception as e:
            return False, f"Erreur critique lors de l'exécution: {e}"

# --- Test rapide du module ---
if __name__ == '__main__':
    # Ce test exécutera le code généré par code_manager.py
    
    # Correction nécessaire ici aussi pour l'exécution directe!
    # L'ajout à sys.path au début du fichier s'applique au main du module
    
    tester = CodeTester()
    success, output = tester.run_tests()
    
    print("\n--- RÉSULTAT DU TEST ---")
    if success:
        print("✅ SUCCÈS : Tous les tests ont passé.")
    else:
        print("❌ ÉCHEC : Des erreurs ont été trouvées.")
        print("\n--- Sortie complète du test ---\n", output)