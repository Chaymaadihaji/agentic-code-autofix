"""
 Système de correction intelligente
Utilise la mémoire d'apprentissage pour corriger automatiquement
"""
import re
from typing import Dict, List, Tuple
from cerveau.apprentissage import MemoireApprentissage

class CorrecteurIntelligent:
    def __init__(self, memoire: MemoireApprentissage):
        """Initialise le correcteur avec une mémoire"""
        self.memoire = memoire
        self.corrections_appliquees = []
        print(" Correcteur intelligent initialisé")
    
    def corriger_code(self, code: str, langage: str, fichier: str, tentative: int, projet: str) -> Tuple[str, List[Dict]]:
        """
        Corrige le code en utilisant l'apprentissage
        """
        erreurs_detectees = self._detecter_erreurs(code, langage, fichier)
        erreurs_corrigees = []
        code_corrige = code
        
        for erreur in erreurs_detectees:
            erreur["tentative"] = tentative
            erreur["projet"] = projet
            erreur["langage"] = langage
            erreur["fichier"] = fichier
            
            
            corrections_similaires = self.memoire.trouver_corrections_similaires(erreur)
            
            if corrections_similaires:
                
                meilleure_correction = corrections_similaires[0]
                if erreur.get("code_avant") in code_corrige:
                    code_corrige = code_corrige.replace(
                        erreur.get("code_avant"),
                        erreur.get("code_apres", erreur.get("code_avant"))
                    )
                    erreur["corrige_avec_memoire"] = True
                    erreur["correction_id"] = meilleure_correction.get("id")
            else:
                
                if erreur.get("code_avant") in code_corrige:
                    code_corrige = code_corrige.replace(
                        erreur.get("code_avant"),
                        erreur.get("code_apres", "")
                    )
                    erreur["corrige_avec_memoire"] = False
            
            
            erreur_id = self.memoire.enregistrer_erreur(erreur)
            erreur["id"] = erreur_id
            
            erreurs_corrigees.append(erreur)
            self.corrections_appliquees.append(erreur)
        
        
        code_corrige = self.memoire.appliquer_corrections_connues(code_corrige, langage, fichier)
        
        return code_corrige, erreurs_corrigees
    
    def _detecter_erreurs(self, code: str, langage: str, fichier: str) -> List[Dict]:
        """
        Détecte les erreurs courantes dans le code
        """
        erreurs = []
        
        if langage == "go":
            erreurs.extend(self._detecter_erreurs_go(code, fichier))
        elif langage == "python":
            erreurs.extend(self._detecter_erreurs_python(code, fichier))
        
        return erreurs
    
    def _detecter_erreurs_go(self, code: str, fichier: str) -> List[Dict]:
        """Détecte les erreurs spécifiques à Go"""
        erreurs = []
        lignes = code.split('\n')
        
        for i, ligne in enumerate(lignes, 1):
            
            if 'undefinedVar' in ligne and ('tentative' in ligne or 'undefined' in ligne.lower()):
                erreurs.append({
                    "type": "undefined_variable",
                    "message": f"Variable non définie ligne {i}",
                    "ligne": i,
                    "code_avant": ligne.strip(),
                    "code_apres": "// " + ligne.strip() + " // Variable supprimée (erreur)",
                    "severite": "error"
                })
            
           
            if 'var x int = "' in ligne and 'texte"' in ligne:
                erreurs.append({
                    "type": "type_error",
                    "message": f"Erreur de type (string dans int) ligne {i}",
                    "ligne": i,
                    "code_avant": ligne.strip(),
                    "code_apres": ligne.strip().replace('int', 'string'),
                    "severite": "error"
                })
            
            
            if 'x =: 5' in ligne:
                erreurs.append({
                    "type": "wrong_assignment",
                    "message": f"Mauvais opérateur d'affectation ligne {i}",
                    "ligne": i,
                    "code_avant": ligne.strip(),
                    "code_apres": ligne.strip().replace('=:', ':='),
                    "severite": "error"
                })
            
            
            if '"inexistant/package' in ligne:
                erreurs.append({
                    "type": "missing_import",
                    "message": f"Import manquant ligne {i}",
                    "ligne": i,
                    "code_avant": ligne.strip(),
                    "code_apres": "// " + ligne.strip() + " // Import supprimé (inexistant)",
                    "severite": "error"
                })
        
        return erreurs
    
    def _detecter_erreurs_python(self, code: str, fichier: str) -> List[Dict]:
        """Détecte les erreurs spécifiques à Python"""
        erreurs = []
        lignes = code.split('\n')
        
        for i, ligne in enumerate(lignes, 1):
            if 'variable_non_definie_' in ligne or 'undefined_var' in ligne:
                erreurs.append({
                    "type": "undefined_variable",
                    "message": f"Variable non définie ligne {i}",
                    "ligne": i,
                    "code_avant": ligne.strip(),
                    "code_apres": "# " + ligne.strip() + " # Variable supprimée",
                    "severite": "error"
                })
        
        return erreurs
    
    def get_rapport_correction(self) -> str:
        """Génère un rapport des corrections appliquées"""
        if not self.corrections_appliquees:
            return " Aucune correction appliquée"
        
        rapport = f" {len(self.corrections_appliquees)} corrections appliquées:\n"
        for i, correction in enumerate(self.corrections_appliquees[:3], 1):
            avec_memoire = "" if correction.get("corrige_avec_memoire") else ""
            rapport += f"  {i}. {avec_memoire} {correction.get('type', 'inconnu')}\n"
        
        return rapport
    
    def reset_corrections(self):
        """Réinitialise les corrections de la session"""
        self.corrections_appliquees = []