# lance_app.py
import os
import sys
import webbrowser
import threading
import time

def lancer_application_flask(chemin_projet):
    """Lance l'application Flask et ouvre le navigateur"""
    print(f"🚀 Lancement de l'application Flask: {chemin_projet}")
    
    # Vérifier que le projet existe
    if not os.path.exists(chemin_projet):
        print(f"❌ Le projet {chemin_projet} n'existe pas")
        return
    
    # Chercher le fichier principal
    fichiers = os.listdir(chemin_projet)
    fichiers_py = [f for f in fichiers if f.endswith(".py")]
    
    for nom_prefere in ["app.py", "main.py", "application.py"]:
        if nom_prefere in fichiers_py:
            fichier_principal = nom_prefere
            break
    else:
        fichier_principal = fichiers_py[0] if fichiers_py else None
    
    if not fichier_principal:
        print("❌ Aucun fichier Python trouvé!")
        return
    
    print(f"🎯 Fichier principal: {fichier_principal}")
    
    # Lire le code pour vérifier
    chemin_fichier = os.path.join(chemin_projet, fichier_principal)
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        code = f.read()
    
    print("\n✅ Application Flask prête à démarrer")
    print("   URL: http://localhost:5000")
    print("   CTRL+C pour arrêter")
    
    # Ouvrir le navigateur après un délai
    def ouvrir_navigateur():
        time.sleep(3)  # Attendre que Flask démarre
        print("\n🌐 Ouverture du navigateur...")
        webbrowser.open("http://localhost:5000")
    
    # Démarrer le thread pour ouvrir le navigateur
    browser_thread = threading.Thread(target=ouvrir_navigateur)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Démarrer Flask
    print("\n" + "="*60)
    print("🔥 SERVEUR FLASK EN COURS D'EXÉCUTION")
    print("="*60 + "\n")
    
    # Exécuter Flask
    os.chdir(chemin_projet)
    os.system(f'python {fichier_principal}')

if __name__ == "__main__":
    # Lancer notre application corrigée
    chemin_projet = "projets/créer_un_330843_221fa1"
    
    print("="*60)
    print("🤖 GESTIONNAIRE DE TÂCHES - APPLICATION FLASK")
    print("="*60)
    print("\n📋 Fonctionnalités:")
    print("   ✅ Liste interactive des tâches")
    print("   ✅ Statistiques de progression")
    print("   ✅ Ajout de nouvelles tâches")
    print("   ✅ Suppression de tâches")
    print("   ✅ Filtrage par statut")
    print("   ✅ Tri des tâches")
    print("\n🔧 Technologies:")
    print("   • Flask (Backend Python)")
    print("   • HTML/CSS/JavaScript (Frontend)")
    print("   • API REST pour les opérations")
    print("="*60)
    
    lancer_application_flask(chemin_projet)