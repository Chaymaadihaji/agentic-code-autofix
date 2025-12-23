# debug_flask_app.py
import os
import sys

def debug_flask_app(chemin_projet):
    """Debug détaillé de l'application Flask"""
    print(f"🔧 DEBUG de l'application Flask: {chemin_projet}")
    
    # 1. Lire app.py
    app_path = os.path.join(chemin_projet, "app.py")
    with open(app_path, 'r', encoding='utf-8') as f:
        app_code = f.read()
    
    print("\n📄 CODE APP.PY COMPLET:")
    print("=" * 60)
    print(app_code)
    print("=" * 60)
    
    # 2. Vérifier le template index.html
    template_path = os.path.join(chemin_projet, "templates", "index.html")
    if os.path.exists(template_path):
        print("\n📄 TEMPLATE INDEX.HTML:")
        print("=" * 60)
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Vérifier les erreurs courantes
        if '{{' in template_content and '}}' not in template_content:
            print("⚠️  Variable Jinja2 non fermée détectée!")
        
        if '{%' in template_content and '%}' not in template_content:
            print("⚠️  Tag Jinja2 non fermé détectée!")
        
        # Afficher les premières 50 lignes
        lines = template_content.split('\n')
        for i, line in enumerate(lines[:50]):
            print(f"{i+1:3}: {line}")
        if len(lines) > 50:
            print(f"... ({len(lines)-50} lignes supplémentaires)")
        print("=" * 60)
    else:
        print("\n❌ Fichier templates/index.html non trouvé!")
        print("Création d'un template simple...")
        
        # Créer un template simple
        simple_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestionnaire de Tâches</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .task { border: 1px solid #ccc; padding: 10px; margin: 5px; }
        .completed { background-color: #d4edda; }
        .in-progress { background-color: #fff3cd; }
    </style>
</head>
<body>
    <h1>Gestionnaire de Tâches</h1>
    
    <h2>Statistiques</h2>
    <p>Total: {{ total }}</p>
    <p>En cours: {{ en_cours }}</p>
    <p>Terminées: {{ terminée }}</p>
    
    <h2>Tâches</h2>
    <div id="tasks">
        {% for data in datas %}
        <div class="task {% if data.status == 'Terminée' %}completed{% else %}in-progress{% endif %}">
            <h3>{{ data.title }}</h3>
            <p>{{ data.description }}</p>
            <p><strong>Statut:</strong> {{ data.status }}</p>
        </div>
        {% endfor %}
    </div>
    
    <h2>Ajouter une tâche</h2>
    <form action="/ajout" method="POST">
        <input type="text" name="title" placeholder="Titre" required><br>
        <textarea name="description" placeholder="Description"></textarea><br>
        <select name="status">
            <option value="En cours">En cours</option>
            <option value="Terminée">Terminée</option>
        </select><br>
        <button type="submit">Ajouter</button>
    </form>
</body>
</html>'''
        
        os.makedirs(os.path.join(chemin_projet, "templates"), exist_ok=True)
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(simple_template)
        print("✅ Template simple créé")
    
    # 3. Vérifier les erreurs dans le code Python
    print("\n🔍 VÉRIFICATION DU CODE PYTHON:")
    
    # Vérifier la fonction calcul_statistiques
    if 'def calcul_statistiques' in app_code:
        print("✅ Fonction calcul_statistiques trouvée")
    
    # Vérifier les problèmes potentiels dans les routes
    lines = app_code.split('\n')
    for i, line in enumerate(lines):
        # Vérifier les références à 'datas' dans les fonctions
        if 'datas = [' in line and i > 0 and 'def' in lines[i-1]:
            print(f"⚠️  Ligne {i+1}: Redéfinition de 'datas' dans une fonction")
            print(f"   Contexte: {lines[i-1:i+2]}")
    
    # 4. Proposer une correction
    print("\n🔧 CORRECTION PROPOSÉE:")
    
    # Le problème est probablement dans les fonctions qui redéfinissent 'datas'
    # Créer une version corrigée
    corrected_code = app_code
    
    # Corriger la fonction supprimer (ligne 40)
    if 'datas = [data for data in datas' in app_code:
        print("⚠️  Problème détecté: Redéfinition de 'datas' dans supprimer()")
        corrected_code = corrected_code.replace(
            '    datas = [data for data in datas if data["id"] != int(id)]',
            '    global datas\n    datas = [data for data in datas if data["id"] != int(id)]'
        )
    
    # Corriger la fonction filtrer (ligne 47)
    if 'datas = [data for data in datas if data["status"] == status]' in app_code:
        print("⚠️  Problème détecté: Redéfinition de 'datas' dans filtrer()")
        corrected_code = corrected_code.replace(
            '    datas = [data for data in datas if data["status"] == status]',
            '    filtered_datas = [data for data in datas if data["status"] == status]\n    return jsonify({"datas": filtered_datas})'
        )
    
    # Sauvegarder la version corrigée
    if corrected_code != app_code:
        backup_path = app_path + ".backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(app_code)
        print(f"✅ Backup créé: {backup_path}")
        
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(corrected_code)
        print("✅ Code corrigé sauvegardé")
        
        print("\n📋 CHANGEMENTS APPLIQUÉS:")
        print("1. Ajouté 'global datas' dans la fonction supprimer()")
        print("2. Corrigé la fonction filtrer() pour éviter de modifier 'datas'")
    
    # 5. Tester l'application corrigée
    print("\n🚀 TEST DE L'APPLICATION CORRIGÉE:")
    
    # Importer et exécuter l'application
    sys.path.insert(0, chemin_projet)
    
    try:
        # Créer un test minimal
        test_code = '''
import sys
sys.path.insert(0, r"%s")

try:
    from app import app
    
    # Tester le client Flask
    with app.test_client() as client:
        print("🧪 Test de la route /")
        response = client.get("/")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Route / fonctionnelle")
            print(f"   Longueur réponse: {len(response.data)} octets")
        else:
            print(f"❌ Erreur {response.status_code}")
            
        print("\\n🧪 Test de l'API /ajout (POST)")
        response = client.post("/ajout", data={
            "title": "Test",
            "description": "Description test",
            "status": "En cours"
        })
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.get_json()}")
        
except Exception as e:
    print(f"❌ Erreur lors du test: {e}")
    import traceback
    traceback.print_exc()
''' % chemin_projet
        
        exec(test_code)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    debug_flask_app("projets/créer_un_330843_221fa1")