#!/usr/bin/env python3
"""
 Module de validation d'applications
Vérifie la cohérence entre frontend et backend
"""

import os
import re
import json

class ValidateurApplication:
    def __init__(self):
        self.erreurs = []
        self.avertissements = []
    
    def valider_projet(self, chemin_projet):
        """Valide l'intégrité d'un projet complet"""
        print(f"   🔍 Validation du projet: {os.path.basename(chemin_projet)}")
        
        self.erreurs = []
        self.avertissements = []
        
       
        self._valider_structure(chemin_projet)
        
    
        self._valider_coherence_api(chemin_projet)
        
       
        if not self.erreurs:
            print(f"    Validation PASSÉE")
            return {"succes": True, "message": "Projet valide"}
        else:
            print(f"     Problèmes détectés: {len(self.erreurs)}")
            for erreur in self.erreurs[:3]: 
                print(f"      - {erreur}")
            return {
                "succes": False, 
                "erreurs": self.erreurs, 
                "avertissements": self.avertissements
            }
    
    def _valider_structure(self, chemin_projet):
        """Vérifie la structure minimale du projet"""
        fichiers_necessaires = ['main.py', 'requirements.txt']
        for fichier in fichiers_necessaires:
            if not os.path.exists(os.path.join(chemin_projet, fichier)):
                self.avertissements.append(f"Fichier recommandé manquant: {fichier}")
    
    def _valider_coherence_api(self, chemin_projet):
        """Vérifie que les APIs appelées dans le frontend existent dans le backend"""
        
     
        routes_api = set()
        for fichier in os.listdir(chemin_projet):
            if fichier.endswith('.py'):
                chemin = os.path.join(chemin_projet, fichier)
                try:
                    with open(chemin, 'r', encoding='utf-8', errors='ignore') as f:
                        contenu = f.read()
                       
                        routes = re.findall(r"@app\.route\(['\"]([^'\"]+)['\"]\)", contenu)
                        routes_api.update(routes)
                except:
                    continue
        
        
        appels_api = set()
        templates_dir = os.path.join(chemin_projet, "templates")
        
        if os.path.exists(templates_dir):
            for template in os.listdir(templates_dir):
                if template.endswith('.html'):
                    chemin = os.path.join(templates_dir, template)
                    try:
                        with open(chemin, 'r', encoding='utf-8', errors='ignore') as f:
                            contenu = f.read()
                           
                            fetches = re.findall(r"fetch\(['\"]([^'\"]+)['\"]\)", contenu)
                            axios = re.findall(r"axios\.(?:get|post)\(['\"]([^'\"]+)['\"]\)", contenu)
                            ajax = re.findall(r"\$\.ajax\([^)]*url:\s*['\"]([^'\"]+)['\"]", contenu)
                            appels_api.update(fetches + axios + ajax)
                    except:
                        continue
        
      
        for appel in appels_api:
            if appel.startswith('/'):
                if appel not in routes_api and not appel.startswith('http'):
                    self.erreurs.append(f"API manquante: '{appel}' appelé dans HTML mais pas dans Flask")
        
       
        if not routes_api and appels_api:
            self.erreurs.append("Routes Flask manquantes pour les appels API détectés")
    
    def get_corrections(self):
        """Retourne les corrections suggérées"""
        corrections = []
        
        for erreur in self.erreurs:
            if "API manquante" in erreur:
               
                match = re.search(r"API manquante: '([^']+)'", erreur)
                if match:
                    url = match.group(1)
                    correction = {
                        "type": "ajout_route",
                        "url": url,
                        "code": f"""@app.route('{url}')
def {self._generer_nom_fonction(url)}():
    return jsonify({{
        "status": "success",
        "endpoint": "{url}",
        "message": "Endpoint ajouté par validation"
    }})"""
                    }
                    corrections.append(correction)
        
        return corrections
    
    def _generer_nom_fonction(self, url):
        """Génère un nom de fonction à partir d'une URL"""
       
        nom = url.replace('/', '_').replace('-', '_').strip('_')
        if not nom:
            nom = 'endpoint'
        return f"{nom}_endpoint"


def test_rapide():
    """Test rapide du validateur"""
    print(" Test du ValidateurApplication")
    
  
    test_dir = "test_validation"
    os.makedirs(test_dir, exist_ok=True)
    
   
    with open(os.path.join(test_dir, "main.py"), "w") as f:
        f.write("""from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/test')
def api_test():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run()
""")
    
    
    os.makedirs(os.path.join(test_dir, "templates"), exist_ok=True)
    with open(os.path.join(test_dir, "templates", "index.html"), "w") as f:
        f.write("""
<script>
fetch('/api/test')  // OK
fetch('/api/missing')  // Problème
</script>
""")
    
   
    validateur = ValidateurApplication()
    resultat = validateur.valider_projet(test_dir)
    
    print(f"Résultat: {resultat}")
    
   
    import shutil
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_rapide()