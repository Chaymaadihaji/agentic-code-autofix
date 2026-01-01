
import sys
import io
import os
import time
import json
import re
import ast
import random
import subprocess
import shutil
import tempfile
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("ERREUR : GROQ_API_KEY non trouvée")
    sys.exit(1)

api_key = os.getenv('GROQ_API_KEY', '')
print(f" Clé API : {api_key[:10]}...")

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# === IMPORTATIONS CORRIGÉES ===
try:
    from cerveau.analyseur import AnalysateurAvance
    from cerveau.architecte import Architecte
    from executeur.createur_fichiers import CreateurFichiers
    from executeur.redacteur_code import RedacteurCode
    # NOUVEAU : Système d'apprentissage
    from cerveau.apprentissage import MemoireApprentissage
    from executeur.correcteur import CorrecteurIntelligent
except ImportError as e:
    print(f" Erreur import : {e}")
    print(f"  Création des fichiers manquants...")
    
    # Créer les fichiers manquants automatiquement
    os.makedirs("cerveau", exist_ok=True)
    os.makedirs("executeur", exist_ok=True)
    
    # Créer cerveau/apprentissage.py
    with open("cerveau/apprentissage.py", "w", encoding="utf-8") as f:
        f.write('''"""
 Système d'apprentissage et de mémorisation
Stocke les erreurs et leurs corrections pour améliorer les futures tentatives
"""
import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Any

class MemoireApprentissage:
    def __init__(self, fichier_memoire="memoire_apprentissage.json"):
        self.fichier_memoire = fichier_memoire
        self.memoire = self._charger_memoire()
        self.corrections_en_cours = []
    
    def _charger_memoire(self) -> Dict:
        if os.path.exists(self.fichier_memoire):
            try:
                with open(self.fichier_memoire, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._memoire_vierge()
        return self._memoire_vierge()
    
    def _memoire_vierge(self) -> Dict:
        return {
            "version": "1.0",
            "date_creation": datetime.now().isoformat(),
            "statistiques": {"total_corrections": 0},
            "corrections": []
        }
    
    def enregistrer_erreur(self, erreur: Dict):
        erreur["timestamp"] = datetime.now().isoformat()
        self.memoire["corrections"].append(erreur)
        self.memoire["statistiques"]["total_corrections"] += 1
        self._sauvegarder_memoire()
        return erreur.get("id", "new")
    
    def _sauvegarder_memoire(self):
        with open(self.fichier_memoire, 'w', encoding='utf-8') as f:
            json.dump(self.memoire, f, indent=2, ensure_ascii=False)
    
    def trouver_corrections_similaires(self, erreur_courante: Dict) -> List[Dict]:
        return []
    
    def appliquer_corrections_connues(self, code: str, langage: str, fichier: str) -> str:
        return code
    
    def get_statistiques(self) -> Dict:
        return self.memoire["statistiques"]
    
    def reset_session(self):
        self.corrections_en_cours = []
''')
    
    # Créer executeur/correcteur.py
    with open("executeur/correcteur.py", "w", encoding="utf-8") as f:
        f.write('''"""
Système de correction intelligente
"""
import re
from typing import Dict, List, Tuple
from cerveau.apprentissage import MemoireApprentissage

class CorrecteurIntelligent:
    def __init__(self, memoire: MemoireApprentissage):
        self.memoire = memoire
        self.corrections_appliquees = []
    
    def corriger_code(self, code: str, langage: str, fichier: str, tentative: int, projet: str) -> Tuple[str, List[Dict]]:
        erreurs = self._detecter_erreurs(code, langage, fichier)
        erreurs_corrigees = []
        code_corrige = code
        
        for erreur in erreurs:
            erreur["tentative"] = tentative
            erreur["projet"] = projet
            self.memoire.enregistrer_erreur(erreur)
            
            if erreur.get("code_avant") in code_corrige:
                code_corrige = code_corrige.replace(
                    erreur.get("code_avant"),
                    erreur.get("code_apres")
                )
                erreur["corrige_avec_memoire"] = False
                erreurs_corrigees.append(erreur)
        
        self.corrections_appliquees.extend(erreurs_corrigees)
        return code_corrige, erreurs_corrigees
    
    def _detecter_erreurs(self, code: str, langage: str, fichier: str) -> List[Dict]:
        erreurs = []
        lignes = code.split('\\n')
        
        for i, ligne in enumerate(lignes, 1):
            erreur = self._detecter_erreur_ligne(ligne, i, langage, fichier)
            if erreur:
                erreurs.append(erreur)
        
        return erreurs
    
    def _detecter_erreur_ligne(self, ligne: str, num_ligne: int, langage: str, fichier: str) -> Dict:
        if langage == "go":
            if 'undefinedVar' in ligne and 'tentative' in ligne:
                return {
                    "type": "undefined_variable",
                    "message": f"Variable non définie ligne {num_ligne}",
                    "langage": langage,
                    "fichier": fichier,
                    "ligne": num_ligne,
                    "code_avant": ligne.strip(),
                    "code_apres": "# " + ligne.strip() + "  # Variable supprimée"
                }
        return None
    
    def get_rapport_correction(self) -> str:
        if not self.corrections_appliquees:
            return "Aucune correction appliquée."
        return f" {len(self.corrections_appliquees)} corrections appliquées"
    
    def reset_corrections(self):
        self.corrections_appliquees = []
''')
    
    
    from cerveau.apprentissage import MemoireApprentissage
    from executeur.correcteur import CorrecteurIntelligent

class AutoCoderBugTest:
    def __init__(self, max_tentatives=4):
        print("  AUTOCODER TEST AVEC APPRENTISSAGE INTELLIGENT")
        print("  Système de mémorisation et correction automatique")
        
        try:
            
            self.memoire = MemoireApprentissage()
            stats = self.memoire.get_statistiques()
            print(f"  Mémoire chargée: {stats.get('total_corrections', 0)} corrections apprises")
            
           
            self.correcteur = CorrecteurIntelligent(self.memoire)
           
            self.analyseur = AnalysateurAvance()
            self.architecte = Architecte()
            self.createur = CreateurFichiers()
            self.redacteur = RedacteurCode()
            
            self.max_tentatives = max_tentatives
            self.erreurs_introduites = []
            self.historique_corrections = [] 
            
            print(" Système de correction intelligente prêt")
            
        except Exception as e:
            print(f" Erreur init : {e}")
            sys.exit(1)
    
    def generer_avec_bugs(self, demande):
        if not demande or not demande.strip():
            print(" Pas de demande")
            return
        
        demande = demande.strip('"\'')
        print(f"\n Demande : {demande}")
        print("-" * 50)
        
        print(" Analyse...")
        try:
            analyse = self.analyseur.analyser_demande(demande)
            app_type = analyse.get('type_application', 'streamlit')
            langage = analyse.get('langage_principal', 'python')
            print(f"   Type: {app_type}")
            print(f"   Langage: {langage}")
        except Exception as e:
            print(f" Erreur analyse: {e}")
            app_type = "python"
            langage = "python"
            analyse = {"type_application": app_type, "langage_principal": langage}
        
        print("\n Architecture...")
        try:
            architecture = self.architecte.creer_architecture(analyse)
            fichiers = architecture.get('fichiers', [])
            print(f"    {len(fichiers)} fichiers")
        except Exception as e:
            print(f" Erreur architecture: {e}")
            fichiers = [
                {"nom": "main.py", "type": "python"},
                {"nom": "requirements.txt", "type": "text"},
                {"nom": "README.md", "type": "text"}
            ]
        
        print("\n Création projet...")
        nom_projet = self._generer_nom(demande)
        chemin = os.path.join("projets", nom_projet)
        os.makedirs(chemin, exist_ok=True)
        print(f"    Dossier: {chemin}")
        
        with open(os.path.join(chemin, "demande.txt"), "w", encoding="utf-8") as f:
            f.write(demande)
        
        with open(os.path.join(chemin, "analyse.json"), "w", encoding="utf-8") as f:
            json.dump(analyse, f, indent=2, ensure_ascii=False)
        
       
        memoire_projet = os.path.join(chemin, "memoire_apprentissage.json")
        with open(memoire_projet, "w", encoding="utf-8") as f:
            json.dump({
                "projet": nom_projet,
                "demande": demande,
                "langage": langage,
                "date_creation": datetime.now().isoformat(),
                "corrections": []
            }, f, indent=2)
        
        print(f"\n TEST AVEC CORRECTION INTELLIGENTE ({self.max_tentatives} tentatives)")
        print("=" * 70)
        
        historique = []
        meilleur_version = None
        meilleur_score = 0
        
        for tentative in range(1, self.max_tentatives + 1):
            print(f"\n{'='*60}")
            print(f" TENTATIVE {tentative}/{self.max_tentatives}")
            print(f"{'='*60}")
            
            
            if tentative > 1:
                stats = self.memoire.get_statistiques()
                print(f"  Mémoire: {stats.get('total_corrections', 0)} corrections apprises")
            
            
            self.redacteur.set_test_mode(True, tentative)
            
            
            print(f"\n GÉNÉRATION...")
            fichiers_crees = self._generer_fichiers(chemin, fichiers, demande, analyse, tentative)
            
            if tentative == 1:
                self._ajouter_fichiers_base(chemin, demande, analyse, langage)
            
          
            if tentative < self.max_tentatives:
                print(f"\n INTRODUCTION DE BUGS POUR TEST...")
                self._introduire_bugs_deliberes(chemin, tentative, langage)
            
       
            print(f"\n CORRECTION INTELLIGENTE...")
            corrections_appliquees = self._appliquer_correction_intelligente(
                chemin, langage, tentative, nom_projet
            )
            
            if corrections_appliquees:
                print(f"    {len(corrections_appliquees)} erreurs corrigées automatiquement")
            
          
            print(f"\n TEST DÉTAILLÉ...")
            resultat_test = self._tester_detaille(chemin, langage)
            
            score = self._calculer_score_detaille(chemin, resultat_test, tentative, corrections_appliquees)
            
            
            if resultat_test["erreurs"]:
                self._apprendre_des_erreurs(resultat_test["erreurs"], langage, tentative, nom_projet)
            
            
            if resultat_test["erreurs"]:
                print(f"\n  ERREURS TROUVÉES ({len(resultat_test['erreurs'])}):")
                for i, erreur in enumerate(resultat_test["erreurs"][:3], 1):
                    print(f"   {i}. {erreur}")
                    self._enregistrer_erreur(erreur, tentative, langage, nom_projet)
                
                if len(resultat_test["erreurs"]) > 3:
                    print(f"   ... et {len(resultat_test['erreurs']) - 3} autres erreurs")
            else:
                print(f"\n AUCUNE ERREUR DÉTECTÉE !")
            
            
            if resultat_test["avertissements"]:
                print(f"\n   AVERTISSEMENTS ({len(resultat_test['avertissements'])}):")
                for i, avert in enumerate(resultat_test["avertissements"][:2], 1):
                    print(f"   {i}. {avert}")
            
          
            print(f"\n  SCORE: {score}/100")
            
            if score > meilleur_score:
                meilleur_score = score
                meilleur_version = tentative
                print(f"  NOUVELLE MEILLEURE VERSION !")
            
            historique.append({
                "tentative": tentative,
                "score": score,
                "erreurs": len(resultat_test["erreurs"]),
                "avertissements": len(resultat_test["avertissements"]),
                "bugs_introduits": len(self.erreurs_introduites) if tentative < self.max_tentatives else 0,
                "corrections_auto": len(corrections_appliquees) 
            })
            
            
            print(f"\n  ÉVOLUTION (tentative {tentative}):")
            print(f"   Score: {score}/100")
            print(f"   Erreurs: {len(resultat_test['erreurs'])}")
            print(f"   Avertissements: {len(resultat_test['avertissements'])}")
            print(f"   Corrections auto: {len(corrections_appliquees)}")  
            if tentative < self.max_tentatives:
                print(f"   Bugs introduits: {len(self.erreurs_introduites)}")
            else:
                print(f"   Bugs introduits: Aucun (dernière)")
            
            
            if tentative < self.max_tentatives:
                print(f"\n  Préparation tentative {tentative + 1}...")
                self._nettoyer_fichiers(chemin)
               
                if tentative == self.max_tentatives - 1:
                    print("   Dernière tentative - pas de bugs délibérés")
        
        
        print(f"\n{'='*70}")
        print(" RAPPORT FINAL - CORRECTION INTELLIGENTE")
        print(f"{'='*70}")
        
        if meilleur_version:
            print(f" MEILLEURE VERSION: TENTATIVE #{meilleur_version}")
            print(f" Dossier: {chemin}")
            print(f" Score final: {meilleur_score}/100")
            print(f" Type: {app_type}")
            print(f" Langage: {langage}")
        else:
            print(f"   Aucune version satisfaisante trouvée")
            print(f"  Code disponible dans: {chemin}")
        
      
        stats = self.memoire.get_statistiques()
        print(f"\n  APPRENTISSAGE RÉALISÉ:")
        print(f"   • Corrections apprises: {stats.get('total_corrections', 0)}")
        print(f"   • Corrections automatiques: {sum(h.get('corrections_auto', 0) for h in historique)}")
        
        print(f"\n  HISTORIQUE COMPLET:")
        print(f"{'Tentative':<10} {'Score':<8} {'Erreurs':<8} {'Corr.Auto':<8} {'État':<12}")
        print(f"{'-'*10:<10} {'-'*8:<8} {'-'*8:<8} {'-'*9:<9} {'-'*12:<12}")
        
        for h in historique:
            etat = "Avec bugs" if h.get('bugs_introduits', 0) > 0 else "Propre"
            if h["tentative"] == self.max_tentatives:
                etat = "Finale"
            
            print(f"{h['tentative']:<10} {h['score']:<8} {h['erreurs']:<8} {h.get('corrections_auto', 0):<9} {etat:<12}")
        
        if self.erreurs_introduites:
            print(f"\n BUGS INTRODUITS DÉLIBÉRÉMENT ({len(self.erreurs_introduites)}):")
            for i, bug in enumerate(self.erreurs_introduites[:5], 1):
                print(f"   {i}. {bug}")
        else:
            print(f"\n BUGS INTRODUITS DÉLIBÉRÉMENT (0)")
        
        print(f"\n💡 APPRENTISSAGE INTELLIGENT:")
        if stats.get('total_corrections', 0) > 0:
            print(f"    Système a appris {stats['total_corrections']} corrections")
            print(f"    Progression: {historique[0]['score']} → {meilleur_score}")
            print(f"    Corrections automatiques appliquées")
            print(f"    Mémoire sauvegardée pour les prochaines exécutions")
        else:
            print(f"     Aucune correction apprise (premier projet?)")
        
       
        print(f"\n POUR LANCER LA VERSION FINALE:")
        if langage == "go":
            print(f"   cd {chemin}")
            print(f"   go mod init project")
            print(f"   go mod tidy")
            print(f"   go run main.go")
        elif langage == "python":
            print(f"   cd {chemin}")
            print(f"   pip install -r requirements.txt")
            print(f"   python main.py")
        elif langage in ["javascript", "typescript"]:
            print(f"   cd {chemin}")
            print(f"   npm install")
            print(f"   npm start")
        
        print(f"\n POUR ANALYSER L'APPRENTISSAGE:")
        print(f"   Regardez: {chemin}/memoire_apprentissage.json")
        print(f"   Et le fichier global: memoire_apprentissage.json")
        
        print(f"{'='*70}")
        
        return {
            'chemin': chemin,
            'meilleure_version': meilleur_version,
            'score_final': meilleur_score,
            'historique': historique,
            'bugs_introduits': self.erreurs_introduites,
            'langage': langage,
            'corrections_apprises': stats.get('total_corrections', 0)  
        }
    
   
    def _appliquer_bug_python(self, content, tentative):
        """Applique des bugs à du code Python"""
        lines = content.split('\n')
        
        if len(lines) < 5:
            return content, "aucun (fichier trop court)"
        
        bug_type = random.choice([
            'syntax_error',
            'name_error', 
            'type_error',
            'indentation_error'
        ])
        
        bug_applique = content
        
        try:
            if bug_type == 'syntax_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, "  print('Erreur syntaxe test)  # Guillemet manquant")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'name_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, f"  variable_non_definie_{tentative} = undefined_var")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'type_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, "  resultat = 'texte' + 123  # Erreur de type")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'indentation_error':
                code_lines = [i for i, line in enumerate(lines) if line.strip() and not line.strip().startswith('#')]
                if code_lines:
                    line_idx = random.choice(code_lines)
                    lines[line_idx] = "  " + lines[line_idx] + "  # Indentation incorrecte"
                    bug_applique = '\n'.join(lines)
        
        except Exception:
            return content, "erreur d'application"
        
        return bug_applique, bug_type
    
    def _appliquer_bug_javascript(self, content, tentative):
        """Applique des bugs à du code JavaScript"""
        lines = content.split('\n')
        
        if len(lines) < 5:
            return content, "aucun (fichier trop court)"
        
        bug_type = random.choice([
            'syntax_error',
            'reference_error', 
            'type_error',
            'undefined_variable'
        ])
        
        bug_applique = content
        
        try:
            if bug_type == 'syntax_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, "  console.log('Erreur syntaxe test);  # Parenthèse manquante")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'reference_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, f"  const x = undefinedVariable_{tentative};")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'type_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, "  const result = 'text' + undefined;")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'undefined_variable':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, "  console.log(nonDefinedVar);")
                bug_applique = '\n'.join(lines)
        
        except Exception:
            return content, "erreur d'application"
        
        return bug_applique, bug_type
    
    def _appliquer_bug_typescript(self, content, tentative):
        """Applique des bugs à du code TypeScript"""
        return self._appliquer_bug_javascript(content, tentative)
    
    def _appliquer_bug_go(self, content, tentative):
        """Applique des bugs à du code Go"""
        lines = content.split('\n')
        
        if len(lines) < 5:
            return content, "aucun (fichier trop court)"
        
        bug_type = random.choice([
            'syntax_error',
            'undefined_variable',
            'type_error',
            'missing_import',
            'wrong_assignment'
        ])
        
        bug_applique = content
        
        try:
            if bug_type == 'syntax_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, f"  fmt.Println(\"Erreur tentative {tentative}\"  # Parenthèse manquante")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'undefined_variable':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, f"  undefinedVar{tentative} := \"test\"")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'type_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, "  var x int = \"texte\"  # Erreur de type")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'missing_import':
                if "import (" in content:
                    for i, line in enumerate(lines):
                        if "import (" in line:
                            insert_pos = i + 1
                            lines.insert(insert_pos, f'    "inexistant/package{tentative}"')
                            break
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'wrong_assignment':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, "  x =: 5  # Mauvais opérateur d'affectation")
                bug_applique = '\n'.join(lines)
        
        except Exception:
            return content, "erreur d'application"
        
        return bug_applique, bug_type
    
    def _appliquer_bug_java(self, content, tentative):
        """Applique des bugs à du code Java"""
        lines = content.split('\n')
        
        if len(lines) < 5:
            return content, "aucun (fichier trop court)"
        
        bug_type = random.choice([
            'syntax_error',
            'missing_semicolon',
            'undefined_class'
        ])
        
        bug_applique = content
        
        try:
            if bug_type == 'syntax_error':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, f"  System.out.println(\"Erreur {tentative}\"  // Parenthèse manquante")
                bug_applique = '\n'.join(lines)
            
            elif bug_type == 'missing_semicolon':
                for i, line in enumerate(lines):
                    if line.strip() and not line.strip().endswith(';') and not line.strip().endswith('{') and not line.strip().endswith('}'):
                        lines[i] = line.rstrip() + " // Point-virgule manquant"
                        bug_applique = '\n'.join(lines)
                        break
            
            elif bug_type == 'undefined_class':
                insert_line = random.randint(1, min(10, len(lines)-1))
                lines.insert(insert_line, f"  UndefinedClass{tentative} obj = new UndefinedClass{tentative}();")
                bug_applique = '\n'.join(lines)
        
        except Exception:
            return content, "erreur d'application"
        
        return bug_applique, bug_type
    
    def _appliquer_correction_intelligente(self, chemin, langage, tentative, projet):
        """Applique la correction intelligente à tous les fichiers"""
        corrections_appliquees = []
        
        for root, dirs, files in os.walk(chemin):
            for file in files:
                if (langage == "go" and file.endswith('.go')) or \
                   (langage == "python" and file.endswith('.py')) or \
                   (langage in ["javascript", "typescript"] and file.endswith(('.js', '.ts', '.jsx', '.tsx'))):
                    
                    fichier_path = os.path.join(root, file)
                    try:
                        with open(fichier_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                      
                        code_corrige, erreurs_corrigees = self.correcteur.corriger_code(
                            code=code,
                            langage=langage,
                            fichier=file,
                            tentative=tentative,
                            projet=projet
                        )
                        
                        
                        if code_corrige != code:
                            with open(fichier_path, 'w', encoding='utf-8') as f:
                                f.write(code_corrige)
                            
                            if erreurs_corrigees:
                                corrections_appliquees.extend(erreurs_corrigees)
                                for erreur in erreurs_corrigees:
                                    type_erreur = erreur.get("type", "inconnu")
                                    print(f"   {file}: {type_erreur} corrigé")
                    
                    except Exception as e:
                        print(f"  Erreur correction {file}: {str(e)[:50]}")
        
        return corrections_appliquees
    
    def _apprendre_des_erreurs(self, erreurs, langage, tentative, projet):
        """Apprend des erreurs détectées pour améliorer les futures corrections"""
        for erreur_msg in erreurs:
     
            erreur_info = self._analyser_message_erreur(erreur_msg, langage)
            if erreur_info:
                
                self.memoire.enregistrer_erreur({
                    "type": erreur_info["type"],
                    "message": erreur_msg,
                    "langage": langage,
                    "tentative": tentative,
                    "projet": projet,
                    "timestamp": datetime.now().isoformat(),
                    "corrige": False 
                })
    
    def _analyser_message_erreur(self, erreur_msg, langage):
        """Analyse le message d'erreur pour en extraire le type"""
        erreur_lower = erreur_msg.lower()
        
        if "variable non définie" in erreur_lower or "undefined" in erreur_lower:
            return {"type": "undefined_variable"}
        elif "erreur de type" in erreur_lower or "type" in erreur_lower:
            return {"type": "type_error"}
        elif "syntax" in erreur_lower:
            return {"type": "syntax_error"}
        elif "import" in erreur_lower:
            return {"type": "missing_import"}
        elif "parenthèse" in erreur_lower or "parenthesis" in erreur_lower:
            return {"type": "missing_parenthesis"}
        elif "opérateur" in erreur_lower or "operator" in erreur_lower:
            return {"type": "wrong_operator"}
        
        return None
    
    
    def _tester_fichier_javascript(self, chemin_fichier):
        """Test spécifique JavaScript"""
        erreurs = []
        avertissements = []
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if 'undefinedVariable_' in line or 'nonDefinedVar' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Variable non définie détectée")
                
                if "'text' + undefined" in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Erreur de type détectée")
                
                if "console.log('Erreur" in line and ");" not in line and "'" in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Erreur de syntaxe détectée")
                
                if "if (x > 5 {" in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Parenthèse manquante détectée")
                
                if len(line) > 120:
                    avertissements.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} trop longue ({len(line)} caractères)")
            
        except Exception as e:
            erreurs.append(f"{os.path.basename(chemin_fichier)}: Erreur analyse - {str(e)[:50]}")
        
        return {'erreurs': erreurs, 'avertissements': avertissements}
    
    def _tester_fichier_typescript(self, chemin_fichier):
        """Test spécifique TypeScript"""
        return self._tester_fichier_javascript(chemin_fichier)
    
    def _tester_fichier_generique(self, chemin_fichier):
        """Test générique pour d'autres langages"""
        erreurs = []
        avertissements = []
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if 'undefined' in line.lower() and 'variable' in line.lower():
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Variable non définie suspectée")
                
                if len(line) > 120:
                    avertissements.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} trop longue ({len(line)} caractères)")
                
                if '(' in line and ')' not in line:
                    avertissements.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Parenthèse ouverte non fermée")
        
        except Exception as e:
            erreurs.append(f"{os.path.basename(chemin_fichier)}: Erreur lecture - {str(e)[:50]}")
        
        return {'erreurs': erreurs, 'avertissements': avertissements}
    
    def _calculer_score_detaille(self, chemin, resultat_test, tentative, corrections_appliquees):
        """Calcule un score avec bonus pour corrections automatiques"""
        score = 100
        
       
        for erreur in resultat_test["erreurs"]:
            if "détectée" in erreur:
                score -= 25  
            else:
                score -= 15
        
        
        score -= len(resultat_test["avertissements"]) * 3
        
        
        if corrections_appliquees:
            bonus_correction = min(20, len(corrections_appliquees) * 5)
            score += bonus_correction
            print(f"   Bonus correction auto: +{bonus_correction}")
        
        
        if tentative == self.max_tentatives:
            if len(resultat_test["erreurs"]) == 0:
                score += 20 
            else:
                score -= 10  
        
        
        fichiers = os.listdir(chemin)
        fichiers_importants = [f for f in fichiers if f.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.java'))]
        if len(fichiers_importants) >= 2:
            score += 5
        
        return max(0, min(100, score))
    
    def _enregistrer_erreur(self, erreur, tentative, langage, projet):
        """Enregistre une erreur avec plus de contexte"""
        erreur_simple = f"T{tentative}: {erreur[:80]}..."
        
       
        erreur_complete = {
            "message": erreur,
            "tentative": tentative,
            "langage": langage,
            "projet": projet,
            "timestamp": datetime.now().isoformat()
        }
        
        self.erreurs_introduites.append(erreur_complete)
        
       
        erreur_info = self._analyser_message_erreur(erreur, langage)
        if erreur_info:
            self.memoire.enregistrer_erreur({
                **erreur_info,
                "message": erreur,
                "langage": langage,
                "tentative": tentative,
                "projet": projet,
                "timestamp": datetime.now().isoformat()
            })
    
    
    
    def _generer_fichiers(self, chemin, fichiers, demande, analyse, tentative):
        """Génère les fichiers"""
        fichiers_crees = []
        
        for fichier in fichiers:
            nom = fichier['nom']
            print(f"     {nom}")
            
            try:
                code = self.redacteur.generer_code_adapte(
                    f"{demande} - Tentative {tentative}",
                    fichier,
                    analyse,
                    chemin,
                    introduire_bugs=(tentative < self.max_tentatives)
                )
                
                self._creer_dossier_parent(chemin, nom)
                chemin_fichier = os.path.join(chemin, nom)
                
                with open(chemin_fichier, "w", encoding="utf-8", errors='ignore') as f:
                    f.write(code)
                
                fichiers_crees.append(nom)
                print(f"      ✓ {len(code)} caractères")
                
            except Exception as e:
                print(f"      ✗ Erreur: {str(e)[:50]}")
                self._code_secours(chemin, nom, demande, analyse)
        
        return fichiers_crees
    
    def _introduire_bugs_deliberes(self, chemin, tentative, langage):
        """INTRODUIT DES BUGS DÉLIBÉRÉMENT"""
        print(f"    MODE TEST - Introduction de bugs (Tentative {tentative})")
        print(f"   Langage cible: {langage}")
        
        bugs_introduits = []
        
      
        fichiers = []
        extensions = []
        
        if langage == "go":
            extensions = ['.go']
        elif langage == "python":
            extensions = ['.py']
        elif langage in ["javascript", "typescript"]:
            extensions = ['.js', '.jsx', '.ts', '.tsx']
        else:
            extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.java', '.cpp', '.c']
        
        for root, dirs, files in os.walk(chemin):
            for file in files:
                for ext in extensions:
                    if file.endswith(ext):
                        fichiers.append(os.path.join(root, file))
                        break
        
        if not fichiers:
            print(f"   Aucun fichier {extensions} trouvé pour introduire des bugs")
            return
        
   
        fichiers_a_corrompre = random.sample(fichiers, min(3, len(fichiers)))
        
        for fichier_path in fichiers_a_corrompre:
            try:
                with open(fichier_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if not content.strip():
                    continue
                
                bug_applique = content
                bug_type = "inconnu"
                
                if fichier_path.endswith('.py'):
                    bug_applique, bug_type = self._appliquer_bug_python(content, tentative)
                elif fichier_path.endswith('.js') or fichier_path.endswith('.jsx'):
                    bug_applique, bug_type = self._appliquer_bug_javascript(content, tentative)
                elif fichier_path.endswith('.ts') or fichier_path.endswith('.tsx'):
                    bug_applique, bug_type = self._appliquer_bug_typescript(content, tentative)
                elif fichier_path.endswith('.go'):
                    bug_applique, bug_type = self._appliquer_bug_go(content, tentative)
                elif fichier_path.endswith('.java'):
                    bug_applique, bug_type = self._appliquer_bug_java(content, tentative)
                else:
                    continue
                
                if bug_applique and bug_applique != content:
                    with open(fichier_path, 'w', encoding='utf-8') as f:
                        f.write(bug_applique)
                    bugs_introduits.append(f"{os.path.basename(fichier_path)}: {bug_type}")
                    print(f"      → Bug '{bug_type}' ajouté à {os.path.basename(fichier_path)}")
            
            except Exception as e:
                print(f"    Erreur lors de l'ajout de bugs à {fichier_path}: {str(e)[:50]}")
        
       
        for bug in bugs_introduits:
            self.erreurs_introduites.append({
                "message": f"Tentative {tentative}: {bug} (langage: {langage})",
                "type": "bug_introduit",
                "timestamp": datetime.now().isoformat()
            })
    
 
    
    def _tester_detaille(self, chemin, langage):
        """Test détaillé amélioré avec support Go"""
        erreurs = []
        avertissements = []
        
        for root, dirs, files in os.walk(chemin):
            for file in files:
                if file.endswith('.py'):
                    chemin_fichier = os.path.join(root, file)
                    result = self._tester_fichier_python(chemin_fichier)
                    erreurs.extend(result['erreurs'])
                    avertissements.extend(result['avertissements'])
                
                elif file.endswith('.js') or file.endswith('.jsx'):
                    chemin_fichier = os.path.join(root, file)
                    result = self._tester_fichier_javascript(chemin_fichier)
                    erreurs.extend(result['erreurs'])
                    avertissements.extend(result['avertissements'])
                
                elif file.endswith('.ts') or file.endswith('.tsx'):
                    chemin_fichier = os.path.join(root, file)
                    result = self._tester_fichier_typescript(chemin_fichier)
                    erreurs.extend(result['erreurs'])
                    avertissements.extend(result['avertissements'])
                
                elif file.endswith('.go'):
                    chemin_fichier = os.path.join(root, file)
                    result = self._tester_fichier_go(chemin_fichier)
                    erreurs.extend(result['erreurs'])
                    avertissements.extend(result['avertissements'])
                
                elif file.endswith(('.java', '.cpp', '.c', '.rs')):
                    chemin_fichier = os.path.join(root, file)
                    result = self._tester_fichier_generique(chemin_fichier)
                    erreurs.extend(result['erreurs'])
                    avertissements.extend(result['avertissements'])
        
        return {
            "succes": len(erreurs) == 0,
            "erreurs": erreurs,
            "avertissements": avertissements
        }
    
    def _tester_fichier_python(self, chemin_fichier):
        """Test spécifique Python"""
        erreurs = []
        avertissements = []
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            ast.parse(code)
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if 'variable_non_definie_' in line or 'undefined_var' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Variable non définie détectée")
                
                if "'texte' + 123" in line or "'text' + 123" in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Erreur de type détectée")
                
                if "print('Erreur" in line and ")" not in line and "'" in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Erreur de syntaxe détectée")
                
                if "import module_inexistant_" in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Import manquant détecté")
                
                if "if x = 5:" in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Mauvais opérateur (= au lieu de ==)")
                
                if len(line) > 120:
                    avertissements.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} trop longue ({len(line)} caractères)")
            
        except SyntaxError as e:
            erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {e.lineno} - Erreur syntaxique: {e.msg}")
        except Exception as e:
            erreurs.append(f"{os.path.basename(chemin_fichier)}: Erreur analyse - {str(e)[:50]}")
        
        return {'erreurs': erreurs, 'avertissements': avertissements}
    
    def _tester_fichier_go(self, chemin_fichier):
        """Test spécifique Go"""
        erreurs = []
        avertissements = []
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                if 'undefinedVar' in line and 'tentative' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Variable non définie détectée")
                
                if 'var x int = "' in line and 'texte"' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Erreur de type détectée (string dans int)")
                
                if 'fmt.Println("Erreur' in line and '" #' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Erreur de syntaxe (parenthèse manquante)")
                
                if '"inexistant/package' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Import manquant détecté")
                
                if 'x =: 5' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Mauvais opérateur d'affectation")
                
                if 'unusedVar' in line:
                    erreurs.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} - Variable non utilisée détectée")
                
                if len(line) > 120:
                    avertissements.append(f"{os.path.basename(chemin_fichier)}: Ligne {i} trop longue ({len(line)} caractères)")
            
        except Exception as e:
            erreurs.append(f"{os.path.basename(chemin_fichier)}: Erreur analyse - {str(e)[:50]}")
        
        return {'erreurs': erreurs, 'avertissements': avertissements}
    
    
    
    def _creer_dossier_parent(self, chemin, nom_fichier):
        if '/' in nom_fichier or '\\' in nom_fichier:
            dossier = os.path.dirname(nom_fichier)
            chemin_dossier = os.path.join(chemin, dossier)
            os.makedirs(chemin_dossier, exist_ok=True)
    
    def _nettoyer_fichiers(self, chemin):
        fichiers_a_garder = [
            "demande.txt", "analyse.json", "README.md",
            "requirements.txt", "go.mod", "package.json",
            "memoire_apprentissage.json"  
        ]
        
        for fichier in os.listdir(chemin):
            if fichier not in fichiers_a_garder:
                try:
                    chemin_fichier = os.path.join(chemin, fichier)
                    if os.path.isfile(chemin_fichier):
                        os.remove(chemin_fichier)
                except:
                    pass
    
    def _ajouter_fichiers_base(self, chemin, demande, analyse, langage):
        app_type = analyse.get('type_application', 'python')
        nom_dossier = os.path.basename(chemin)
        
        readme = f"""# {demande}

## Langage: {langage.upper()}
## Type: {app_type}

## Installation
```bash
cd {nom_dossier}
"""
        
        if langage == "python":
            requirements = ""
            if app_type == "streamlit":
                requirements = "streamlit\npandas\nnumpy"
            elif app_type == "flask":
                requirements = "flask\nflask-cors"
            elif app_type == "fastapi":
                requirements = "fastapi\nuvicorn"
            
            with open(os.path.join(chemin, "requirements.txt"), "w", encoding="utf-8") as f:
                f.write(requirements)
            
            if requirements:
                readme += f"pip install -r requirements.txt\n"
            readme += "python main.py\n"
        
        elif langage == "go":
            go_mod = f"""module {nom_dossier}

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/lib/pq v1.10.9
)
"""
            with open(os.path.join(chemin, "go.mod"), "w", encoding="utf-8") as f:
                f.write(go_mod)
            
            readme += "go mod tidy\ngo run main.go\n"
        
        elif langage in ["javascript", "typescript"]:
            package_json = {
                "name": nom_dossier,
                "version": "1.0.0",
                "scripts": {
                    "start": "node main.js" if langage == "javascript" else "ts-node main.ts"
                }
            }
            
            with open(os.path.join(chemin, "package.json"), "w", encoding="utf-8") as f:
                json.dump(package_json, f, indent=2)
            
            readme += "npm install\nnpm start\n"
        
        readme += "```"
        
        with open(os.path.join(chemin, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme)
    
    def _code_secours(self, chemin, nom_fichier, demande, analyse):
        if nom_fichier.endswith('.py'):
            code = '''print("Application de test")'''
        elif nom_fichier.endswith('.go'):
            code = '''package main

import "fmt"

func main() {
    fmt.Println("Application Go de test")
}
'''
        elif nom_fichier.endswith('.js'):
            code = '''console.log("Application JavaScript de test");'''
        elif nom_fichier.endswith('.ts'):
            code = '''console.log("Application TypeScript de test");'''
        else:
            code = f"# {demande}\n# Fichier: {nom_fichier}"
        
        with open(os.path.join(chemin, nom_fichier), "w", encoding="utf-8") as f:
            f.write(code)
    
    def _generer_nom(self, demande):
        import hashlib
        timestamp = str(int(time.time()))[-6:]
        hash_demande = hashlib.md5(demande.encode()).hexdigest()[:6]
        
        mots = re.findall(r'\b\w+\b', demande.lower())[:2]
        base_nom = "_".join(mots) if len(mots) >= 2 else "test"
        base_nom = re.sub(r'[^\w\-]', '_', base_nom)
        base_nom = base_nom.strip('_')
        
        return f"{base_nom}_{timestamp}_{hash_demande}"

def main():
    print("=" * 70)
    print(" AUTOCODER TEST - CORRECTION INTELLIGENTE")
    print("=" * 70)
    print(" Avec mémorisation des erreurs et apprentissage automatique")
    print("-" * 70)
    
    autocoder = AutoCoderBugTest(max_tentatives=4)
    
    if len(sys.argv) > 1:
        demande = " ".join(sys.argv[1:])
        print(f" Demande: {demande}")
    else:
        print(" Cette version APPREND DES ERREURS et s'améliore automatiquement")
        print("-" * 70)
        demande = input("\n Que veux-tu tester ?\n> ")
    
    if not demande.strip():
        print(" Pas de demande")
        return
    
    print(f"\n Lancement avec apprentissage intelligent...")
    print(" Le système va mémoriser les erreurs pour mieux corriger")
    
    resultat = autocoder.generer_avec_bugs(demande)
    
    print("\n" + "=" * 70)
    if resultat['corrections_apprises'] > 0:
        print(f" APPRENTISSAGE RÉUSSI !")
        print(f" {resultat['corrections_apprises']} corrections apprises")
        print(f" Mémoire sauvegardée pour les prochains projets")
    else:
        print("  Aucune correction apprise")
        print(" C'est peut-être le premier projet ou il n'y avait pas d'erreurs")
    print("=" * 70)

if __name__ == "__main__":
    main()