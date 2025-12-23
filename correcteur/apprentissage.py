"""
🎓 Module d'apprentissage des erreurs
"""

import json
import os
import datetime

class Apprentissage:
    def __init__(self):
        self.chemin_connaissances = "connaissances/solutions"
        os.makedirs(self.chemin_connaissances, exist_ok=True)
    
    def apprendre_erreur(self, erreur, correction):
        """
        Apprend d'une erreur et de sa correction
        """
        # Créer un ID unique pour cette erreur
        from hashlib import md5
        erreur_id = md5(erreur.encode()).hexdigest()[:8]
        
        fichier_erreur = os.path.join(self.chemin_connaissances, f"erreur_{erreur_id}.json")
        
        donnees = {
            "erreur": erreur[:500],
            "correction": correction,
            "date": datetime.datetime.now().isoformat(),
            "utilisations": 1
        }
        
        # Si le fichier existe déjà, incrémenter les utilisations
        if os.path.exists(fichier_erreur):
            try:
                with open(fichier_erreur, "r") as f:
                    existant = json.load(f)
                    donnees["utilisations"] = existant.get("utilisations", 0) + 1
            except:
                pass
        
        # Sauvegarder
        with open(fichier_erreur, "w") as f:
            json.dump(donnees, f, indent=2)
        
        print(f"✅ Erreur apprise et sauvegardée: {fichier_erreur}")
    
    def enregistrer_reussite(self, demande, chemin_projet, tentatives):
        """
        Enregistre un projet réussi
        """
        reussites_dir = os.path.join("connaissances", "reussites")
        os.makedirs(reussites_dir, exist_ok=True)
        
        from hashlib import md5
        projet_id = md5(demande.encode()).hexdigest()[:8]
        
        donnees = {
            "demande": demande,
            "chemin": chemin_projet,
            "tentatives": tentatives,
            "date": datetime.datetime.now().isoformat(),
            "statut": "reussi"
        }
        
        fichier = os.path.join(reussites_dir, f"projet_{projet_id}.json")
        with open(fichier, "w") as f:
            json.dump(donnees, f, indent=2)
    
    def chercher_solution(self, erreur):
        """
        Cherche une solution connue pour une erreur
        """
        if not os.path.exists(self.chemin_connaissances):
            return None
        
        from hashlib import md5
        erreur_id = md5(erreur.encode()).hexdigest()[:8]
        fichier_potentiel = os.path.join(self.chemin_connaissances, f"erreur_{erreur_id}.json")
        
        if os.path.exists(fichier_potentiel):
            try:
                with open(fichier_potentiel, "r") as f:
                    return json.load(f)
            except:
                pass
        
        # Chercher par similarité (basique)
        for fichier in os.listdir(self.chemin_connaissances):
            if fichier.endswith(".json"):
                try:
                    with open(os.path.join(self.chemin_connaissances, fichier), "r") as f:
                        solution = json.load(f)
                        if any(mot in erreur for mot in solution.get("erreur", "").split()[:3]):
                            return solution
                except:
                    continue
        
        return None