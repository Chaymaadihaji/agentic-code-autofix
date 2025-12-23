"""
🔍 Module de détection et analyse de bugs
"""

import re

class DetecteurBugs:
    def __init__(self):
        self.patterns_erreurs = {
            "ModuleNotFoundError": r"ModuleNotFoundError: No module named '(\w+)'",
            "ImportError": r"ImportError: (.*)",
            "SyntaxError": r"SyntaxError: (.*)",
            "NameError": r"NameError: name '(\w+)' is not defined",
            "IndentationError": r"IndentationError: (.*)",
            "FileNotFoundError": r"FileNotFoundError: (.*)",
            "AttributeError": r"AttributeError: (.*)",
            "TypeError": r"TypeError: (.*)",
            "KeyError": r"KeyError: (.*)",
            "IndexError": r"IndexError: (.*)"
        }
    
    def analyser_erreur(self, message_erreur):
        """
        Analyse un message d'erreur pour en extraire l'information
        """
        bugs = {
            "type": "inconnu",
            "module": None,
            "variable": None,
            "message": message_erreur[:200],  # Limiter la taille
            "suggestions": []
        }
        
        # Chercher des patterns connus
        for type_erreur, pattern in self.patterns_erreurs.items():
            match = re.search(pattern, message_erreur)
            if match:
                bugs["type"] = type_erreur
                
                if type_erreur == "ModuleNotFoundError":
                    bugs["module"] = match.group(1)
                    bugs["suggestions"] = [
                        f"Installer le module avec: pip install {match.group(1)}",
                        f"Ajouter '{match.group(1)}' à requirements.txt"
                    ]
                elif type_erreur == "NameError":
                    bugs["variable"] = match.group(1)
                    bugs["suggestions"] = [
                        f"Définir la variable '{match.group(1)}'",
                        f"Vérifier l'orthographe de '{match.group(1)}'",
                        f"Importer le module contenant '{match.group(1)}'"
                    ]
                elif type_erreur == "ImportError":
                    bugs["suggestions"] = [
                        "Vérifier le nom du module importé",
                        "Vérifier si le module est installé",
                        "Corriger le chemin d'import"
                    ]
                elif type_erreur == "SyntaxError":
                    bugs["suggestions"] = [
                        "Vérifier la syntaxe Python",
                        "Chercher les parenthèses non fermées",
                        "Vérifier les guillemets"
                    ]
                
                break
        
        # Si pas de pattern connu, analyser avec des heuristiques simples
        if bugs["type"] == "inconnu":
            if "not found" in message_erreur.lower():
                bugs["type"] = "FichierManquant"
                bugs["suggestions"] = ["Vérifier le chemin du fichier", "Créer le fichier manquant"]
            elif "permission" in message_erreur.lower():
                bugs["type"] = "PermissionError"
                bugs["suggestions"] = ["Vérifier les permissions du fichier"]
            elif "timeout" in message_erreur.lower():
                bugs["type"] = "Timeout"
                bugs["suggestions"] = ["Augmenter le timeout", "Optimiser le code"]
        
        return bugs