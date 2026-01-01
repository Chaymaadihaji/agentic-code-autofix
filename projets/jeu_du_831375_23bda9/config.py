# config.py
import json

class Config:
    def __init__(self):
        self.dossiers = {
            'mots': 'mots.json',
            'scores': 'scores.json'
        }
        self.mots = self.charger_mots()

    def charger_mots(self):
        with open(self.dossiers['mots'], 'r') as f:
            return json.load(f)

    def sauvegarder_mots(self):
        with open(self.dossiers['mots'], 'w') as f:
            json.dump(self.mots, f)

    def charger_scores(self):
        try:
            with open(self.dossiers['scores'], 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def sauvegarder_scores(self, scores):
        with open(self.dossiers['scores'], 'w') as f:
            json.dump(scores, f)
