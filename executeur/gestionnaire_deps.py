"""
 Module de gestion des dépendances
"""

import os
import subprocess
import sys 

class GestionnaireDeps:
    def __init__(self):
        pass
    
    def installer_dependances(self, chemin_projet, dependances):
        """
        Installe les dépendances Python pour un projet
        """
        print(f"Installation de {len(dependances)} dépendance(s)...")
        
       
        dependances_corrigees = []
        for dep in dependances:
            if not isinstance(dep, str):
                continue
            
            dep_lower = dep.lower()
            
          
            if 'tkinter' in dep_lower:
                print(f"  → Tkinter: généralement inclus avec Python")
                if sys.platform == "darwin":  
                    print(f"      Sur macOS, Tkinter peut nécessiter: brew install python-tk")
                continue  
            
          
            elif 'sqlite' in dep_lower:
                print(f"  → SQLite: intégré à Python, pas besoin d'installation")
                continue
            
            
            elif 'bootstrap' in dep_lower and 'flask' not in dep_lower:
                dependances_corrigees.append('Flask-Bootstrap')
                print(f"  → Transformation: {dep} → Flask-Bootstrap")
            
           
            elif 'matplotlib' in dep_lower:
                dependances_corrigees.append('matplotlib')
            
          
            elif 'dash' in dep_lower:
                dependances_corrigees.extend(['dash', 'plotly', 'pandas'])
                print(f"  → Transformation: {dep} → dash + plotly + pandas")
            
           
            elif 'plotly' in dep_lower:
                dependances_corrigees.append('plotly')
            
           
            elif 'pandas' in dep_lower:
                dependances_corrigees.append('pandas')
            
           
            elif 'via cdn' in dep_lower or 'cdn' in dep_lower:
                print(f"  → {dep}: CDN - pas d'installation pip nécessaire")
                continue
            
            
            elif 'flask' in dep_lower:
                if dep_lower not in ['flask', 'flask-bootstrap']:
                    dependances_corrigees.append(dep)
                else:
                    dependances_corrigees.append('Flask')
            
           
            else:
                dependances_corrigees.append(dep)
        
        
        dependances_corrigees = list(dict.fromkeys(dependances_corrigees))
        
        if not dependances_corrigees:
            print("   Aucune dépendance pip à installer")
            return True
        
        
        requirements_path = os.path.join(chemin_projet, "requirements.txt")
        
        
        
        requirements_existants = []
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, "r", encoding="utf-8") as f:
                    requirements_existants = [line.strip() for line in f if line.strip()]
            except:
                pass
        
       
        nouvelles_deps = []
        for dep in dependances_corrigees:
            if dep not in requirements_existants:
                nouvelles_deps.append(dep)
        
      
        toutes_deps = list(set(requirements_existants + dependances_corrigees))
        with open(requirements_path, "w", encoding="utf-8") as f:
            for dep in toutes_deps:
                f.write(f"{dep}\n")
        
        
        for dep in nouvelles_deps:
            print(f"  → Installation de {dep}...")
            
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=chemin_projet
                )
                
                if result.returncode == 0:
                    print(f"     {dep} installé")
                else:
                    
                    if '[' in dep:
                        dep_base = dep.split('[')[0]
                        print(f"     Erreur avec extras, essai sans...")
                        result2 = subprocess.run(
                            [sys.executable, "-m", "pip", "install", dep_base],
                            capture_output=True,
                            text=True,
                            timeout=60,
                            cwd=chemin_projet
                        )
                        if result2.returncode == 0:
                            print(f"    {dep_base} installé (sans extras)")
                        else:
                            print(f"     Échec installation {dep}: {result2.stderr[:100]}")
                    else:
                        print(f"     Échec installation {dep}: {result.stderr[:100]}")
                        
            except subprocess.TimeoutExpired:
                print(f"     Timeout installation {dep}")
            except Exception as e:
                print(f"     Exception installation {dep}: {e}")
        
       
        self._verifier_installations_critiques(chemin_projet, toutes_deps)
        
        return True
    
    def _verifier_installations_critiques(self, chemin_projet, dependances):
        """Vérifie que les dépendances critiques sont bien installées"""
        print(f"  → Vérification des installations...")
        
        dependances_lower = [d.lower() for d in dependances]
        
        # Vérifier Flask
        if any('flask' in d for d in dependances_lower):
            if self.verifier_installation('flask'):
                print(f"    Flask vérifié")
            else:
                print(f"    Flask peut ne pas être installé correctement")
        
       
        if any('dash' in d for d in dependances_lower):
            if self.verifier_installation('dash'):
                print(f"     Dash vérifié")
            else:
                print(f"    Dash peut ne pas être installé correctement")
        
       
        if any('dash' in d or 'plotly' in d for d in dependances_lower):
            if self.verifier_installation('plotly'):
                print(f"    Plotly vérifié")
            else:
                print(f"     Plotly peut ne pas être installé correctement")
        
        
        if any('dash' in d or 'pandas' in d for d in dependances_lower):
            if self.verifier_installation('pandas'):
                print(f"   Pandas vérifié")
            else:
                print(f"  Pandas peut ne pas être installé correctement")
        
        
        if any('flask-bootstrap' in d or 'bootstrap' in d for d in dependances_lower):
            try:
                test_code = """
try:
    from flask_bootstrap4 import Bootstrap
    print(" Flask-Bootstrap4 disponible")
except ImportError:
    try:
        from flask_bootstrap import Bootstrap
        print(" Flask-Bootstrap (ancien) disponible")
    except ImportError:
        print(" Flask-Bootstrap non disponible")
"""
                result = subprocess.run(
                    [sys.executable, "-c", test_code],
                    capture_output=True,
                    text=True,
                    cwd=chemin_projet
                )
                print(f"    {result.stdout.strip()}")
            except:
                print(f"  Erreur vérification Flask-Bootstrap")
    
    def verifier_installation(self, module):
        """
        Vérifie si un module Python est installé
        """
        try:
            __import__(module.replace("-", "_"))
            return True
        except ImportError:
            return False
    
    def analyser_fichier_pour_dependances(self, chemin_fichier):
        """
        Analyse un fichier Python pour détecter les dépendances nécessaires
        """
        dependances_detectees = []
        
        if not os.path.exists(chemin_fichier):
            return dependances_detectees
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
            
          
            if 'import dash' in contenu or 'from dash' in contenu:
                dependances_detectees.extend(['dash', 'plotly', 'pandas'])
            
            if 'import flask' in contenu or 'from flask' in contenu:
                dependances_detectees.append('Flask')
            
            if 'import plotly' in contenu or 'from plotly' in contenu:
                dependances_detectees.append('plotly')
            
            if 'import pandas' in contenu or 'from pandas' in contenu:
                dependances_detectees.append('pandas')
            
            if 'import matplotlib' in contenu or 'from matplotlib' in contenu:
                dependances_detectees.append('matplotlib')
            
            if 'import numpy' in contenu or 'from numpy' in contenu:
                dependances_detectees.append('numpy')
            
          
            dependances_detectees = list(dict.fromkeys(dependances_detectees))
            
        except:
            pass
        
        return dependances_detectees


if __name__ == "__main__":
    print(" Test du GestionnaireDeps")
    
   
    import tempfile
    temp_dir = tempfile.mkdtemp()
    print(f"Dossier test: {temp_dir}")
    
    
    deps = ["Flask", "matplotlib", "Tkinter", "SQLite", "Bootstrap via CDN", "dash"]
    gestionnaire = GestionnaireDeps()
    resultat = gestionnaire.installer_dependances(temp_dir, deps)
    
    print(f"\n Résultat: {' Succès' if resultat else ' Échec'}")
    
    # Tester l'analyse de fichier
    test_file = os.path.join(temp_dir, "test.py")
    with open(test_file, "w") as f:
        f.write("import dash\nimport pandas\nfrom flask import Flask\n")
    
    deps_detectees = gestionnaire.analyser_fichier_pour_dependances(test_file)
    print(f"\n Dépendances détectées dans test.py: {deps_detectees}")
    
    # Nettoyer
    import shutil
    shutil.rmtree(temp_dir)
    print(f" Dossier nettoyé: {temp_dir}")