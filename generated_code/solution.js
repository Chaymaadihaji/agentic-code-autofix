function soustraire(a, b) {
    return a - b;
}

// Exemple d'utilisation
console.log(soustraire(10, 5));  // Affiche 5

// Version avec classe
class Calculatrice {
    soustraire(a, b) {
        return a - b;
    }
}

// Exemple d'utilisation avec classe
let calc = new Calculatrice();
console.log(calc.soustraire(10, 5));  // Affiche 5