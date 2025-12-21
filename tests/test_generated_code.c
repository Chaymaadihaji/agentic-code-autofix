#include <stdio.h>
#include <string.h>

// Définition de la structure Produit
typedef struct {
    char nom[100];
    int quantite;
} Produit;

// Fonction pour ajouter du stock
void ajouter_stock(Produit* p, int n) {
    p->quantite += n;
}

// Fonction pour vendre un produit
void vendre_produit(Produit* p, int n) {
    if (p->quantite >= n) {
        p->quantite -= n;
    } else {
        printf("Erreur\n");
    }
}

int main() {
    // Création d'un produit
    Produit p;
    strcpy(p.nom, "Test");
    p.quantite = 0;

    // Ajout de 10 unités au stock
    ajouter_stock(&p, 10);

    // Vente de 5 unités
    vendre_produit(&p, 5);

    // Vérification du stock restant
    if (p.quantite == 5) {
        printf("SUCCESS\n");
    } else {
        printf("FAILURE\n");
    }

    return 0;
}