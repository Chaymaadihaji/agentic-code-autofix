"""
📁 Module de création de fichiers et dossiers
"""

import os
import shutil

class CreateurFichiers:
    def __init__(self):
        pass
    
    def creer_structure_projet(self, chemin_projet, architecture):
        """
        Crée la structure complète du projet
        """
        # Créer le dossier principal
        os.makedirs(chemin_projet, exist_ok=True)
        
        # Créer les sous-dossiers
        for dossier in architecture.get("structure_dossiers", []):
            dossier_path = os.path.join(chemin_projet, dossier)
            os.makedirs(dossier_path, exist_ok=True)
        
        # Créer les fichiers (vides pour l'instant)
        for fichier_info in architecture.get("fichiers", []):
            nom_fichier = fichier_info["nom"]
            chemin_fichier = os.path.join(chemin_projet, nom_fichier)
            
            # Créer le fichier avec un contenu minimal
            with open(chemin_fichier, "w") as f:
                if nom_fichier.endswith(".py"):
                    f.write("# Fichier généré par Robot Développeur\n\n")
                elif nom_fichier == "README.md":
                    f.write("# Projet généré automatiquement\n\n")
                elif nom_fichier == "requirements.txt":
                    f.write("# Dépendances Python\n\n")
        
        print(f"Structure créée: {chemin_projet}")
    
    def ecrire_fichier(self, chemin_projet, nom_fichier, contenu):
        """
        Écrit du contenu dans un fichier
        """
        chemin_complet = os.path.join(chemin_projet, nom_fichier)
        
        # Assurer que le dossier parent existe
        os.makedirs(os.path.dirname(chemin_complet), exist_ok=True)
        
        with open(chemin_complet, "w", encoding="utf-8") as f:
            f.write(contenu)
        
        return chemin_complet
    
    def supprimer_projet(self, chemin_projet):
        """
        Supprime un projet complet
        """
        if os.path.exists(chemin_projet):
            shutil.rmtree(chemin_projet)
            return True
        return False