# forms.py

from django import forms
from .models import Tache

class TacheForm(forms.ModelForm):
    """
    Formulaire pour la création et l'édition de tâches.
    """
    class Meta:
        model = Tache
        fields = ('titre', 'description', 'date_echeance')

class StatistiqueForm(forms.Form):
    """
    Formulaire pour l'affichage des statistiques de progression.
    """
    date_debut = forms.DateField(label="Date de début")
    date_fin = forms.DateField(label="Date de fin")

class SuppressionTacheForm(forms.Form):
    """
    Formulaire pour la suppression de tâches.
    """
    id_tache = forms.IntegerField(label="ID de la tâche à supprimer")
