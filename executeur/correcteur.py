"""
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
        lignes = code.split('\n')
        
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
