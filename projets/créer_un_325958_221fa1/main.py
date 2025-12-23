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

        # Création des widgets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame_taches = tk.Frame(self.notebook)
        self.frame_statistiques = tk.Frame(self.notebook)

        self.notebook.add(self.frame_taches, text="Tâches")
        self.notebook.add(self.frame_statistiques, text="Statistiques")

        # Frame Tâches
        self.label_titre_taches = tk.Label(self.frame_taches, text="Liste des tâches", font=("Arial", 18))
        self.label_titre_taches.pack(pady=10)

        self.liste_taches = tk.Listbox(self.frame_taches, width=50)
        self.liste_taches.pack(pady=10)

        self.entry_tache = tk.Entry(self.frame_taches, width=50)
        self.entry_tache.pack(pady=10)

        self.bouton_ajouter_tache = tk.Button(self.frame_taches, text="Ajouter", command=self.ajouter_tache)
        self.bouton_ajouter_tache.pack(pady=10)

        self.bouton_editer_tache = tk.Button(self.frame_taches, text="Éditer", command=self.editer_tache)
        self.bouton_editer_tache.pack(pady=10)

        self.bouton_supprimer_tache = tk.Button(self.frame_taches, text="Supprimer", command=self.supprimer_tache)
        self.bouton_supprimer_tache.pack(pady=10)

        # Frame Statistiques
        self.label_titre_statistiques = tk.Label(self.frame_statistiques, text="Statistiques de progression", font=("Arial", 18))
        self.label_titre_statistiques.pack(pady=10)

        self.label_statistiques = tk.Label(self.frame_statistiques, text="", font=("Arial", 14))
        self.label_statistiques.pack(pady=10)

        self.mettre_a_jour_liste_taches()
        self.mettre_a_jour_statistiques()

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
        tache = self.entry_tache.get()
        if tache:
            self.taches.append({"tache": tache, "terminee": False})
            self.sauvegarder_taches()
            self.mettre_a_jour_liste_taches()
            self.mettre_a_jour_statistiques()
            self.entry_tache.delete(0, tk.END)

    def editer_tache(self):
        try:
            index = self.liste_taches.curselection()[0]
            tache = self.taches[index]
            tache["tache"] = self.entry_tache.get()
            self.sauvegarder_taches()
            self.mettre_a_jour_liste_taches()
            self.mettre_a_jour_statistiques()
            self.entry_tache.delete(0, tk.END)
        except IndexError:
            messagebox.showerror("Erreur", "Sélectionnez une tâche à éditer")

    def supprimer_tache(self):
        try:
            index = self.liste_taches.curselection()[0]
            del self.taches[index]
            self.sauvegarder_taches()
            self.mettre_a_jour_liste_taches()
            self.mettre_a_jour_statistiques()
        except IndexError:
            messagebox.showerror("Erreur", "Sélectionnez une tâche à supprimer")

    def mettre_a_jour_liste_taches(self):
        self.liste_taches.delete(0, tk.END)
        for tache in self.taches:
            self.liste_taches.insert(tk.END, tache["tache"])

    def mettre_a_jour_statistiques(self):
        terminees = sum(1 for tache in self.taches if tache["terminee"])
        total = len(self.taches)
        pourcentage = (terminees / total) * 100 if total > 0 else 0
        self.label_statistiques.config(text=f"{terminees} tâches terminées sur {total} ({pourcentage:.2f}%)")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnaireDeTaches(root)
    root.mainloop()
