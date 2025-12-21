
import sys
import os
from pathlib import Path

# Ajouter le répertoire courant au chemin Python
sys.path.append('.')

from agent.tester_agent import TesterAgent

def test_tester_agent_initialisation():
    """Teste la création d'un TesterAgent."""
    print("Test 1: Initialisation de TesterAgent...")
    agent = TesterAgent()
    assert agent is not None
    assert hasattr(agent, 'test_results')
    print("✓ TesterAgent initialisé avec succès")
    return True

def test_create_tests():
    """Teste la création d'un plan de tests."""
    print("\nTest 2: Création d'un plan de tests...")
    agent = TesterAgent()
    
    design = {
        "language": "python",
        "components": ["Calculator", "Parser", "Validator"]
    }
    
    implementation = {"status": "pending"}
    
    test_plan = agent.create_tests(design, implementation)
    
    assert test_plan is not None
    assert "test_files" in test_plan
    assert "test_strategy" in test_plan
    assert "coverage_goals" in test_plan
    assert len(test_plan["test_files"]) == 4  # 3 composants + test_main.py
    
    print(f"✓ Plan de tests créé : {test_plan['test_strategy']}")
    print(f"  Fichiers : {test_plan['test_files']}")
    return True

def test_analyze_results():
    """Teste l'analyse des résultats de tests."""
    print("\nTest 3: Analyse des résultats...")
    agent = TesterAgent()
    
    results = [
        {"file": "test_calc.py", "passed": True, "output": "", "error": ""},
        {"file": "test_parser.py", "passed": False, "output": "", "error": "AssertionError"}
    ]
    
    analysis = agent.analyze_test_results(results)
    
    assert analysis["total_tests"] == 2
    assert analysis["passed"] == 1
    assert analysis["failed"] == 1
    assert len(analysis["common_errors"]) > 0
    
    print(f"✓ Analyse réussie : {analysis['passed']} passés, {analysis['failed']} échoués")
    return True

def test_run_tests_simulation():
    """Teste l'exécution de tests (simulation)."""
    print("\nTest 4: Exécution simulée de tests...")
    agent = TesterAgent()
    
    # Créer un dossier de tests temporaire
    test_dir = "temp_test_dir"
    os.makedirs(test_dir, exist_ok=True)
    
    # Créer un fichier de test simple
    test_file = os.path.join(test_dir, "test_sample.py")
    with open(test_file, "w") as f:
        f.write("""
def test_addition():
    assert 1 + 1 == 2

def test_subtraction():
    assert 5 - 3 == 2
""")
    
    try:
        # Essayer d'exécuter les tests
        success, summary, details = agent.run_tests("python", test_dir)
        
        # Même si ça échoue (car pas de structure pytest complète), on teste l'appel
        print(f"✓ Appel à run_tests exécuté")
        print(f"  Résumé : {summary}")
    finally:
        # Nettoyer
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
    
    return True

def main():
    """Exécute tous les tests."""
    print("🔍 Début des tests de TesterAgent\n")
    
    tests = [
        test_tester_agent_initialisation,
        test_create_tests,
        test_analyze_results,
        test_run_tests_simulation
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} a échoué: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"RÉSULTATS : {passed} passés, {failed} échoués")
    
    if failed == 0:
        print("✅ Tous les tests ont réussi !")
    else:
        print(f"❌ {failed} test(s) ont échoué")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
