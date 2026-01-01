"""
 Module de planification des étapes de développement
"""

import json
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class Planificateur:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    
    def creer_plan(self, analyse, architecture):
        """
        Crée un plan de développement étape par étape
        """
        prompt = f"""
        Crée un plan de développement étape par étape.
        
        ANALYSE : {json.dumps(analyse, indent=2)}
        ARCHITECTURE : {json.dumps(architecture, indent=2)}
        
        Retourne un JSON avec :
        - etapes : liste d'étapes avec 'ordre', 'description', 'duree_estimee'
        - priorite : "haute", "moyenne", "basse" pour chaque étape
        - dependances : quelles étapes dépendent d'autres
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un planificateur de projet. Retourne uniquement du JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            content = response.choices[0].message.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content)
            
        except Exception as e:
            print(f"Erreur planification: {e}")
            return {
                "etapes": [
                    {"ordre": 1, "description": "Créer la structure de base", "duree_estimee": "5min", "priorite": "haute"},
                    {"ordre": 2, "description": "Implémenter la fonctionnalité principale", "duree_estimee": "15min", "priorite": "haute"},
                    {"ordre": 3, "description": "Ajouter l'interface utilisateur", "duree_estimee": "10min", "priorite": "moyenne"},
                    {"ordre": 4, "description": "Tests et débogage", "duree_estimee": "10min", "priorite": "haute"}
                ]
            }
        


      