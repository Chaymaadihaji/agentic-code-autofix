# src/main.py
from agent.coordinator import Coordinator

def main():
    print("🤖 SYSTÈME MULTI-AGENTS DE GÉNÉRATION DE CODE")
    print("=" * 60)
    
    # Créer le coordinateur
    coordinator = Coordinator(provider="groq")  # Changez en "gemini" si besoin
    
    # Objectif à résoudre
    objectives = [
        "Créer une classe TodoList avec ajouter_tache, terminer_tache, lister_taches et sauvegarde JSON",
        "Créer une fonction qui calcule la factorielle d'un nombre",
        "Créer un système de gestion de contacts avec recherche et tri",
        "Créer une fonction analyser_donnees_mixtes qui prend une liste, extrait tous les nombres entiers et flottants, ignore strictement les booléens, et retourne un dictionnaire avec somme, moyenne et nombre_elements"
    ]
    
    print("\n📋 Objectifs disponibles:")
    for i, obj in enumerate(objectives, 1):
        print(f"  {i}. {obj}")
    
    print("  5. Saisir votre propre objectif")
    
    try:
        choice = int(input("\nChoisissez (1-5): "))
        
        if choice == 5:
            objective = input("Votre objectif: ")
        elif 1 <= choice <= 4:
            objective = objectives[choice - 1]
        else:
            print("❌ Choix invalide, utilisation du défaut")
            objective = objectives[0]
    except:
        objective = objectives[0]
    
    # Résoudre le problème
    print(f"\n🎯 Résolution de: {objective}")
    print("-" * 40)
    
    result = coordinator.solve_problem(objective, max_iterations=3)
    
    # Afficher les résultats
    print(f"\n{'='*60}")
    print("📊 RÉSULTATS FINAUX")
    print(f"{'='*60}")
    
    print(f"Statut: {result['status'].upper()}")
    print(f"Itérations: {result['iterations']}")
    print(f"Langage: {result['design'].get('language', 'python')}")
    
    if result['status'] == 'success':
        print("\n✅ PROBLÈME RÉSOLU!")
        print(f"📁 Code généré dans: generated_code/")
        print(f"🧪 Tests dans: tests/")
    else:
        print("\n⚠️  Solution partielle générée")
        print("🔍 Consultez debug_history/ pour l'analyse")
    
    # Sauvegarder l'historique
    coordinator.save_debug_info()
    
    print(f"\n{'='*60}")
    print("🎯 Fin de l'exécution")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()