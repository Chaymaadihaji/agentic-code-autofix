import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class Tache:
    def __init__(self, titre, description, etat):
        self.titre = titre
        self.description = description
        self.etat = etat

class GestionnaireTaches:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de tâches")
        self.taches = self.charger_taches()
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        self.interface()

    def interface(self):
        # Création de la liste des tâches
        self.liste_taches = tk.Listbox(self.frame)
        self.liste_taches.pack(fill="both", expand=True)
        self.afficher_taches()

        # Création du formulaire de création de tâche
        self.formulaire = tk.Frame(self.frame)
        self.formulaire.pack(fill="x")
        self.titre_label = tk.Label(self.formulaire, text="Titre")
        self.titre_label.pack(side="left")
        self.titre_entry = tk.Entry(self.formulaire)
        self.titre_entry.pack(side="left")
        self.description_label = tk.Label(self.formulaire, text="Description")
        self.description_label.pack(side="left")
        self.description_entry = tk.Entry(self.formulaire)
        self.description_entry.pack(side="left")
        self.creer_bouton = tk.Button(self.formulaire, text="Créer", command=self.creer_tache)
        self.creer_bouton.pack(side="left")

        # Création du bouton d'édition de tâche
        self.editer_bouton = tk.Button(self.frame, text="Éditer", command=self.editer_tache)
        self.editer_bouton.pack(fill="x")

        # Création du bouton de suppression de tâche
        self.supprimer_bouton = tk.Button(self.frame, text="Supprimer", command=self.supprimer_tache)
        self.supprimer_bouton.pack(fill="x")

        # Création du bouton d'affichage des statistiques
        self.statistiques_bouton = tk.Button(self.frame, text="Statistiques", command=self.afficher_statistiques)
        self.statistiques_bouton.pack(fill="x")

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
        self.liste_taches.delete(0, tk.END)
        for tache in self.taches:
            self.liste_taches.insert(tk.END, tache["titre"])

    def creer_tache(self):
        titre = self.titre_entry.get()
        description = self.description_entry.get()
        self.taches.append({"titre": titre, "description": description, "etat": "en cours"})
        self.sauvegarder_taches()
        self.afficher_taches()
        self.titre_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def editer_tache(self):
        selection = self.liste_taches.curselection()
        if selection:
            index = selection[0]
            tache = self.taches[index]
            self.titre_entry.delete(0, tk.END)
            self.titre_entry.insert(0, tache["titre"])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, tache["description"])
            self.creer_bouton.config(text="Modifier", command=lambda: self.modifier_tache(index))
        else:
            messagebox.showerror("Erreur", "Sélectionnez une tâche à éditer")

    def modifier_tache(self, index):
        titre = self.titre_entry.get()
        description = self.description_entry.get()
        self.taches[index] = {"titre": titre, "description": description, "etat": "en cours"}
        self.sauvegarder_taches()
        self.afficher_taches()
        self.titre_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.creer_bouton.config(text="Créer", command=self.creer_tache)

    def supprimer_tache(self):
        selection = self.liste_taches.curselection()
        if selection:
            index = selection[0]
            del self.taches[index]
            self.sauvegarder_taches()
            self.afficher_taches()
        else:
            messagebox.showerror("Erreur", "Sélectionnez une tâche à supprimer")

    def afficher_statistiques(self):
        en_cours = 0
        terminees = 0
        for tache in self.taches:
            if tache["etat"] == "en cours":
                en_cours += 1
            elif tache["etat"] == "terminée":
                terminees += 1
        messagebox.showinfo("Statistiques", f"En cours : {en_cours}\nTerminées : {terminees}")

if __name__ == "__main__":
    root = tk.Tk()
    gestionnaire = GestionnaireTaches(root)
    root.mainloop()
