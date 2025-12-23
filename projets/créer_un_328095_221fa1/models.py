# models.py
from enum import Enum
from datetime import datetime
from random import randint, choice

class Priorite(Enum):
    BASSE = 1
    MÉDIUM = 2
    ÉLEVÉE = 3

class Statut(Enum):
    EN_ATTENTE = 1
    EN_COURS = 2
    TERMINÉ = 3

class Tache:
    def __init__(self, id, titre, description, priorite, statut, date_debut, date_fin, duree):
        self.id = id
        self.titre = titre
        self.description = description
        self.priorite = priorite
        self.statut = statut
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.duree = duree

class Dashboard:
    def __init__(self):
        self.taches = [
            Tache(1, "Tâche 1", "Description 1", Priorite.MÉDIUM, Statut.EN_ATTENTE, datetime(2022, 1, 1), datetime(2022, 1, 15), 10),
            Tache(2, "Tâche 2", "Description 2", Priorite.ÉLEVÉE, Statut.EN_COURS, datetime(2022, 2, 1), datetime(2022, 2, 28), 20),
            Tache(3, "Tâche 3", "Description 3", Priorite.BASSE, Statut.TERMINÉ, datetime(2022, 3, 1), datetime(2022, 3, 15), 5),
            Tache(4, "Tâche 4", "Description 4", Priorite.MÉDIUM, Statut.EN_ATTENTE, datetime(2022, 4, 1), datetime(2022, 4, 20), 15),
            Tache(5, "Tâche 5", "Description 5", Priorite.ÉLEVÉE, Statut.EN_COURS, datetime(2022, 5, 1), datetime(2022, 5, 31), 30)
        ]

    def get_taches(self):
        return self.taches

    def get_statistiques(self):
        return {
            "taches_en_cours": len([tache for tache in self.taches if tache.statut == Statut.EN_COURS]),
            "taches_en_attente": len([tache for tache in self.taches if tache.statut == Statut.EN_ATTENTE]),
            "taches_terminées": len([tache for tache in self.taches if tache.statut == Statut.TERMINÉ]),
            "duree_total": sum([tache.duree for tache in self.taches]),
            "duree_moyenne": sum([tache.duree for tache in self.taches]) / len(self.taches)
        }
