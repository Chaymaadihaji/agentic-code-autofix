# config.py
import json

class Config:
    def __init__(self):
        self.scores_file = 'scores.json'
        self.history_file = 'history.json'

    def load_scores(self):
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'pierre': 0, 'papier': 0, 'ciseaux': 0}

    def save_scores(self, scores):
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f)

    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_history(self, history):
        with open(self.history_file, 'w') as f:
            json.dump(history, f)
