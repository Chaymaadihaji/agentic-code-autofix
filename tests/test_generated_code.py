# tests_todolist.py

"""
Fichier de tests pour la classe TodoList.
"""

import unittest
from todolist import TodoList
import json

class TestTodoList(unittest.TestCase):
    """
    Classe de tests pour la classe TodoList.
    """

    def setUp(self):
        """
        Méthode appelée avant chaque test.
        """
        self.todolist = TodoList()

    def test_ajouter_tache(self):
        """
        Test de la méthode ajouter_tache.
        """
        self.todolist.ajouter_tache("Tâche 1")
        self.todolist.ajouter_tache("Tâche 2")
        self.assertEqual(len(self.todolist.lister_taches()), 2)

    def test_terminer_tache(self):
        """
        Test de la méthode terminer_tache.
        """
        self.todolist.ajouter_tache("Tâche 1")
        self.todolist.ajouter_tache("Tâche 2")
        self.todolist.terminer_tache(0)
        self.assertTrue(self.todolist.lister_taches()[0]["termine"])

    def test_lister_taches(self):
        """
        Test de la méthode lister_taches.
        """
        self.todolist.ajouter_tache("Tâche 1")
        self.todolist.ajouter_tache("Tâche 2")
        taches = self.todolist.lister_taches()
        self.assertEqual(len(taches), 2)
        self.assertEqual(taches[0]["titre"], "Tâche 1")
        self.assertEqual(taches[1]["titre"], "Tâche 2")

    def test_sauvegarde_JSON(self):
        """
        Test de la méthode sauvegarde_JSON.
        """
        self.todolist.ajouter_tache("Tâche 1")
        self.todolist.ajouter_tache("Tâche 2")
        self.todolist.sauvegarde_JSON("donnees.json")
        with open("donnees.json", "r") as fichier:
            donnees = json.load(fichier)
        self.assertEqual(len(donnees), 2)
        self.assertEqual(donnees[0]["titre"], "Tâche 1")
        self.assertEqual(donnees[1]["titre"], "Tâche 2")

if __name__ == "__main__":
    unittest.main()