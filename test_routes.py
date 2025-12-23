# test_flask_app.py
import os
import sys
import requests
import subprocess
import time
import re

def tester_application_flask(chemin_projet):
    """Test spécifique pour applications Flask"""
    print(f"🔍 Test de l'application Flask dans: {chemin_projet}")
    
    # 1. Vérifier que le projet existe
    if not os.path.exists(chemin_projet):
        print(f"❌ Le projet {chemin_projet} n'existe pas")
        print("Projets disponibles dans 'projets/':")
        for item in os.listdir("projets"):
            if os.path.isdir(os.path.join("projets", item)):
                print(f"  - {item}")
        return
    
    # 2. Chercher le fichier principal
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
    
    # 3. Lire le code pour voir les routes
    chemin_fichier = os.path.join(chemin_projet, fichier_principal)
    print(f"\n📄 Analyse du code {fichier_principal}...")
    
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Afficher les premières 50 lignes
        lignes = code.split('\n')
        print(f"📝 Aperçu du code ({len(lignes)} lignes):")
        print("=" * 60)
        for i, ligne in enumerate(lignes[:50]):
            print(f"{i+1:3}: {ligne}")
        if len(lignes) > 50:
            print(f"... ({len(lignes)-50} lignes supplémentaires)")
        print("=" * 60)
        
        # Analyser les routes Flask
        routes = re.findall(r'@app\.route\(["\']([^"\']+)["\']', code)
        print(f"\n🔍 Routes détectées dans le code: {routes}")
        
        # Chercher aussi d'autres patterns
        flask_patterns = [
            (r'@(\w+)\.route\(["\']([^"\']+)["\']', "Autre instance Flask"),
            (r'@blueprint\.route\(["\']([^"\']+)["\']', "Blueprint"),
        ]
        
        for pattern, desc in flask_patterns:
            matches = re.findall(pattern, code)
            if matches:
                print(f"🔍 {desc} détecté: {matches}")
        
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return
    
    # 4. Démarrer Flask en arrière-plan
    print(f"\n🚀 Démarrage du serveur Flask...")
    try:
        process = subprocess.Popen(
            [sys.executable, fichier_principal],
            cwd=chemin_projet,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 5. Attendre le démarrage
        print(f"⏳ Attente du démarrage (7 secondes)...")
        time.sleep(7)
        
        # 6. Tester les routes
        print(f"\n📡 Test des routes sur http://localhost:5000...")
        base_url = 'http://localhost:5000'
        
        # Routes à tester (celles détectées + standards)
        routes_a_tester = set(routes)
        routes_a_tester.update(['/', '/index', '/dashboard', '/tasks', '/api/tasks', 
                              '/api/dashboard', '/api/data', '/api/statistics', '/home'])
        
        print(f"🔧 Test de {len(routes_a_tester)} routes...")
        
        resultats = []
        for route in sorted(routes_a_tester):
            try:
                response = requests.get(f'{base_url}{route}', timeout=3)
                status = f"HTTP {response.status_code}"
                if response.status_code == 200:
                    status += " ✅"
                    if len(response.text) < 200:
                        preview = response.text[:80].replace('\n', ' ').replace('\r', '')
                        status += f" - {preview}..."
                resultats.append((route, status))
            except requests.exceptions.ConnectionError:
                resultats.append((route, "❌ Connexion refusée"))
            except Exception as e:
                resultats.append((route, f"❌ Erreur: {str(e)[:30]}"))
        
        # Afficher les résultats
        print("\n📊 RÉSULTATS DES TESTS:")
        print("-" * 60)
        for route, status in resultats:
            print(f"{route:25} -> {status}")
        print("-" * 60)
        
        # Compter les succès
        succes = sum(1 for _, status in resultats if "✅" in status or "HTTP 200" in status)
        print(f"🎯 {succes}/{len(resultats)} routes accessibles")
        
        # 7. Lire la sortie Flask pour debug
        print(f"\n🔍 Debug - Sortie du serveur Flask:")
        try:
            process.terminate()
            stdout, stderr = process.communicate(timeout=3)
            
            if stdout:
                print("📤 STDOUT (premiers 300 caractères):")
                print(stdout[:300])
                if len(stdout) > 300:
                    print("...")
            
            if stderr:
                print("\n📥 STDERR (premiers 300 caractères):")
                print(stderr[:300])
                if len(stderr) > 300:
                    print("...")
                    
        except:
            print("⚠️ Impossible de lire la sortie du processus")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    # 8. Vérifier la présence de templates
    print(f"\n📁 Structure du projet:")
    for root, dirs, files in os.walk(chemin_projet):
        level = root.replace(chemin_projet, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Limiter à 5 fichiers par dossier
            print(f'{subindent}{file}')
        if len(files) > 5:
            print(f'{subindent}... ({len(files)-5} fichiers supplémentaires)')

if __name__ == "__main__":
    # Testons notre application de gestion de tâches
    chemin_projet = "projets/créer_un_330843_221fa1"
    
    print("🧪 TEST COMPLET DE L'APPLICATION FLASK")
    print("=" * 60)
    
    tester_application_flask(chemin_projet)
    
    print("\n💡 CONSEILS:")
    print("1. Si aucune route ne fonctionne, vérifiez que:")
    print("   - Le fichier app.py a bien une route '/' définie")
    print("   - Le serveur écoute sur le port 5000")
    print("   - Aucune autre application n'utilise le port 5000")
    print("\n2. Pour accéder à l'application:")
    print("   - Ouvrez http://localhost:5000 dans votre navigateur")
    print("   - Essayez les routes détectées dans le test")
    print("\n3. Pour debug:")
    print("   - Vérifiez les logs Flask dans le terminal")
    print("   - Regardez si les templates HTML existent")