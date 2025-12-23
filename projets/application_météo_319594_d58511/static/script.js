// Importation des bibliothèques nécessaires
import { createChart } from 'chart.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';

// Sélection des éléments du DOM
const cartesContainer = document.getElementById('cartes');
const graphiquesContainer = document.getElementById('graphiques');
const villesSelect = document.getElementById('villes-select');

// Fonction d'initialisation des graphiques
const initCharts = () => {
    // Configuration des options pour les graphiques
    const options = {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    // Récupération des données pour les graphiques
    const donnees = [
        { label: 'Température', data: [10, 20, 30, 40, 50] },
        { label: 'Humidité', data: [50, 40, 30, 20, 10] }
    ];

    // Création des graphiques
    donnees.forEach((donnee) => {
        const ctx = document.createElement('canvas');
        graphiquesContainer.appendChild(ctx);
        const chart = createChart(ctx, {
            type: 'line',
            data: {
                labels: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'],
                datasets: [donnee]
            },
            options: options
        });
    });
};

// Fonction de mise en place des cartes
const setupCards = () => {
    // Récupération des données pour les cartes
    const donnees = [
        { ville: 'Paris', temperature: 20, humidite: 50 },
        { ville: 'Lyon', temperature: 25, humidite: 40 },
        { ville: 'Marseille', temperature: 30, humidite: 30 },
        { ville: 'Bordeaux', temperature: 22, humidite: 45 },
        { ville: 'Toulouse', temperature: 28, humidite: 35 }
    ];

    // Création des cartes
    donnees.forEach((donnee) => {
        const carte = document.createElement('div');
        carte.classList.add('card', 'mb-3');
        carte.innerHTML = `
            <h5 class="card-title">${donnee.ville}</h5>
            <p class="card-text">Température : ${donnee.temperature}°C</p>
            <p class="card-text">Humidité : ${donnee.humidite}%</p>
        `;
        cartesContainer.appendChild(carte);
    });
};

// Fonction de gestion des événements utilisateur
const handleUserEvents = () => {
    // Gestion de la sélection des villes
    villesSelect.addEventListener('change', (e) => {
        const villeSelectionnee = e.target.value;
        // Mettre à jour les cartes et les graphiques en fonction de la ville sélectionnée
        updateCardsAndCharts(villeSelectionnee);
    });
};

// Fonction de mise à jour des cartes et des graphiques
const updateCardsAndCharts = (villeSelectionnee) => {
    // Récupération des données pour la ville sélectionnée
    const donnees = [
        { ville: 'Paris', temperature: 20, humidite: 50 },
        { ville: 'Lyon', temperature: 25, humidite: 40 },
        { ville: 'Marseille', temperature: 30, humidite: 30 },
        { ville: 'Bordeaux', temperature: 22, humidite: 45 },
        { ville: 'Toulouse', temperature: 28, humidite: 35 }
    ];

    // Mise à jour des cartes
    const carte = document.querySelector(`[data-ville="${villeSelectionnee}"]`);
    if (carte) {
        const donneeVille = donnees.find((donnee) => donnee.ville === villeSelectionnee);
        carte.innerHTML = `
            <h5 class="card-title">${donneeVille.ville}</h5>
            <p class="card-text">Température : ${donneeVille.temperature}°C</p>
            <p class="card-text">Humidité : ${donneeVille.humidite}%</p>
        `;
    }

    // Mise à jour des graphiques
    const graphique = document.querySelector(`[data-ville="${villeSelectionnee}"]`);
    if (graphique) {
        const donneeVille = donnees.find((donnee) => donnee.ville === villeSelectionnee);
        graphique.innerHTML = `
            <canvas>
                <script>
                    const ctx = document.createElement('canvas');
                    const chart = createChart(ctx, {
                        type: 'line',
                        data: {
                            labels: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'],
                            datasets: [{
                                label: 'Température',
                                data: [10, 20, 30, 40, 50]
                            }]
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                </script>
            </canvas>
        `;
    }
};

// Fonction principale
const main = () => {
    // Initialisation des graphiques
    initCharts();

    // Mise en place des cartes
    setupCards();

    // Gestion des événements utilisateur
    handleUserEvents();
};

// Lancement de la fonction principale
main();
