import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class GestionnaireTaches:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de tâches")
        self.root.geometry("800x600")
        self.taches = self.charger_taches()

        # Création des onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Onglet pour la liste des tâches
        self.onglet_liste = ttk.Frame(self.notebook)
        self.notebook.add(self.onglet_liste, text="Liste des tâches")

        # Onglet pour les statistiques
        self.onglet_statistiques = ttk.Frame(self.notebook)
        self.notebook.add(self.onglet_statistiques, text="Statistiques")

        # Création de la liste des tâches
        self.liste_taches = tk.Listbox(self.onglet_liste)
        self.liste_taches.pack(pady=10)

        # Boutons pour la gestion des tâches
        self.bouton_ajouter = tk.Button(self.onglet_liste, text="Ajouter", command=self.ajouter_tache)
        self.bouton_ajouter.pack(pady=10)

        self.bouton_editer = tk.Button(self.onglet_liste, text="Éditer", command=self.editer_tache)
        self.bouton_editer.pack(pady=10)

        self.bouton_supprimer = tk.Button(self.onglet_liste, text="Supprimer", command=self.supprimer_tache)
        self.bouton_supprimer.pack(pady=10)

        # Création des statistiques
        self.label_statistiques = tk.Label(self.onglet_statistiques, text="Statistiques")
        self.label_statistiques.pack(pady=10)

        self.label_taches_total = tk.Label(self.onglet_statistiques, text="Tâches totales :")
        self.label_taches_total.pack(pady=10)

        self.label_taches_terminees = tk.Label(self.onglet_statistiques, text="Tâches terminées :")
        self.label_taches_terminees.pack(pady=10)

        self.label_taches_en_cours = tk.Label(self.onglet_statistiques, text="Tâches en cours :")
        self.label_taches_en_cours.pack(pady=10)

        # Mise à jour de la liste des tâches
        self.mettre_a_jour_liste_taches()

    def charger_taches(self):
        try:
            with open("taches.json", "r") as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            return []

    def sauvegarder_taches(self):
        with open("taches.json", "w") as fichier:
            json.dump(self.taches, fichier)

    def ajouter_tache(self):
        # Création d'une fenêtre pour ajouter une tâche
        fenetre_ajouter = tk.Toplevel(self.root)
        fenetre_ajouter.title("Ajouter une tâche")

        # Création des champs pour la tâche
        label_nom = tk.Label(fenetre_ajouter, text="Nom de la tâche")
        label_nom.pack(pady=10)

        entry_nom = tk.Entry(fenetre_ajouter)
        entry_nom.pack(pady=10)

        label_description = tk.Label(fenetre_ajouter, text="Description de la tâche")
        label_description.pack(pady=10)

        entry_description = tk.Entry(fenetre_ajouter)
        entry_description.pack(pady=10)

        # Bouton pour ajouter la tâche
        def ajouter():
            nom = entry_nom.get()
            description = entry_description.get()
            self.taches.append({"nom": nom, "description": description, "terminee": False})
            self.sauvegarder_taches()
            self.mettre_a_jour_liste_taches()
            fenetre_ajouter.destroy()

        bouton_ajouter = tk.Button(fenetre_ajouter, text="Ajouter", command=ajouter)
        bouton_ajouter.pack(pady=10)

    def editer_tache(self):
        # Récupération de la tâche sélectionnée
        index = self.liste_taches.curselection()
        if index:
            tache = self.taches[index[0]]

            # Création d'une fenêtre pour éditer la tâche
            fenetre_editer = tk.Toplevel(self.root)
            fenetre_editer.title("Éditer une tâche")

            # Création des champs pour la tâche
            label_nom = tk.Label(fenetre_editer, text="Nom de la tâche")
            label_nom.pack(pady=10)

            entry_nom = tk.Entry(fenetre_editer)
            entry_nom.insert(0, tache["nom"])
            entry_nom.pack(pady=10)

            label_description = tk.Label(fenetre_editer, text="Description de la tâche")
            label_description.pack(pady=10)

            entry_description = tk.Entry(fenetre_editer)
            entry_description.insert(0, tache["description"])
            entry_description.pack(pady=10)

            # Bouton pour éditer la tâche
            def editer():
                nom = entry_nom.get()
                description = entry_description.get()
                self.taches[index[0]] = {"nom": nom, "description": description, "terminee": tache["terminee"]}
                self.sauvegarder_taches()
                self.mettre_a_jour_liste_taches()
                fenetre_editer.destroy()

            bouton_editer = tk.Button(fenetre_editer, text="Éditer", command=editer)
            bouton_editer.pack(pady=10)

    def supprimer_tache(self):
        # Récupération de la tâche sélectionnée
        index = self.liste_taches.curselection()
        if index:
            del self.taches[index[0]]
            self.sauvegarder_taches()
            self.mettre_a_jour_liste_taches()

    def mettre_a_jour_liste_taches(self):
        self.liste_taches.delete(0, tk.END)
        for tache in self.taches:
            self.liste_taches.insert(tk.END, tache["nom"])

        # Mise à jour des statistiques
        taches_total = len(self.taches)
        taches_terminees = sum(1 for tache in self.taches if tache["terminee"])
        taches_en_cours = taches_total - taches_terminees

        self.label_taches_total.config(text=f"Tâches totales : {taches_total}")
        self.label_taches_terminees.config(text=f"Tâches terminées : {taches_terminees}")
        self.label_taches_en_cours.config(text=f"Tâches en cours : {taches_en_cours}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnaireTaches(root)
    root.mainloop()
