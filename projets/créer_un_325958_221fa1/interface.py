import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class GestionnaireDeTaches:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de tâches")
        self.root.geometry("800x600")
        self.taches = self.charger_taches()

        # Création de la frame principale
        self.frame_principale = tk.Frame(self.root)
        self.frame_principale.pack(fill="both", expand=True)

        # Création de la frame pour la liste des tâches
        self.frame_liste_taches = tk.Frame(self.frame_principale)
        self.frame_liste_taches.pack(fill="both", expand=True)

        # Création de la liste des tâches
        self.liste_taches = tk.Listbox(self.frame_liste_taches)
        self.liste_taches.pack(fill="both", expand=True)
        self.afficher_taches()

        # Création de la frame pour les boutons
        self.frame_boutons = tk.Frame(self.frame_principale)
        self.frame_boutons.pack(fill="x")

        # Création des boutons
        self.bouton_ajouter = tk.Button(self.frame_boutons, text="Ajouter", command=self.ajouter_tache)
        self.bouton_ajouter.pack(side="left", fill="x", expand=True)

        self.bouton_editer = tk.Button(self.frame_boutons, text="Éditer", command=self.editer_tache)
        self.bouton_editer.pack(side="left", fill="x", expand=True)

        self.bouton_supprimer = tk.Button(self.frame_boutons, text="Supprimer", command=self.supprimer_tache)
        self.bouton_supprimer.pack(side="left", fill="x", expand=True)

        self.bouton_statistiques = tk.Button(self.frame_boutons, text="Statistiques", command=self.afficher_statistiques)
        self.bouton_statistiques.pack(side="left", fill="x", expand=True)

    def charger_taches(self):
        try:
            with open("taches.json", "r") as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            return []

    def sauvegarder_taches(self):
        with open("taches.json", "w") as fichier:
            json.dump(self.taches, fichier)

    def afficher_taches(self):
        self.liste_taches.delete(0, "end")
        for tache in self.taches:
            self.liste_taches.insert("end", tache["nom"])

    def ajouter_tache(self):
        fenetre_ajouter = tk.Toplevel(self.root)
        fenetre_ajouter.title("Ajouter une tâche")

        label_nom = tk.Label(fenetre_ajouter, text="Nom de la tâche")
        label_nom.pack()

        entry_nom = tk.Entry(fenetre_ajouter)
        entry_nom.pack()

        def ajouter():
            nom = entry_nom.get()
            if nom:
                self.taches.append({"nom": nom, "terminee": False})
                self.sauvegarder_taches()
                self.afficher_taches()
                fenetre_ajouter.destroy()

        bouton_ajouter = tk.Button(fenetre_ajouter, text="Ajouter", command=ajouter)
        bouton_ajouter.pack()

    def editer_tache(self):
        selection = self.liste_taches.curselection()
        if selection:
            index = selection[0]
            tache = self.taches[index]

            fenetre_editer = tk.Toplevel(self.root)
            fenetre_editer.title("Éditer une tâche")

            label_nom = tk.Label(fenetre_editer, text="Nom de la tâche")
            label_nom.pack()

            entry_nom = tk.Entry(fenetre_editer)
            entry_nom.insert(0, tache["nom"])
            entry_nom.pack()

            def editer():
                nom = entry_nom.get()
                if nom:
                    tache["nom"] = nom
                    self.sauvegarder_taches()
                    self.afficher_taches()
                    fenetre_editer.destroy()

            bouton_editer = tk.Button(fenetre_editer, text="Éditer", command=editer)
            bouton_editer.pack()

    def supprimer_tache(self):
        selection = self.liste_taches.curselection()
        if selection:
            index = selection[0]
            del self.taches[index]
            self.sauvegarder_taches()
            self.afficher_taches()

    def afficher_statistiques(self):
        terminees = sum(1 for tache in self.taches if tache.get("terminee", False))
        total = len(self.taches)
        pourcentage = (terminees / total) * 100 if total > 0 else 0

        fenetre_statistiques = tk.Toplevel(self.root)
        fenetre_statistiques.title("Statistiques")

        label_terminees = tk.Label(fenetre_statistiques, text=f"Tâches terminées : {terminees}")
        label_terminees.pack()

        label_total = tk.Label(fenetre_statistiques, text=f"Total de tâches : {total}")
        label_total.pack()

        label_pourcentage = tk.Label(fenetre_statistiques, text=f"Pourcentage de tâches terminées : {pourcentage:.2f}%")
        label_pourcentage.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnaireDeTaches(root)
    root.mainloop()
