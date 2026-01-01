# Bibliothèque en ligne avec Spring Boot et PostgreSQL

## Présentation

Cette application est une bibliothèque en ligne qui permet de gérer une collection de livres. Elle offre des fonctionnalités de CRUD pour les livres, recherche par titre, auteur et catégorie, gestion des emprunts de livres, authentification JWT et documentation Swagger/OpenAPI.

## Fonctionnalités

### Fonctionnalité principale

* Gérer les livres :
 + Créer un livre : `/livres` (POST)
 + Lire les livres : `/livres` (GET)
 + Mettre à jour un livre : `/livres/{id}` (PUT)
 + Supprimer un livre : `/livres/{id}` (DELETE)
* Rechercher des livres :
 + Par titre : `/livres?titre={titre}` (GET)
 + Par auteur : `/livres?auteur={auteur}` (GET)
 + Par catégorie : `/livres?categorie={categorie}` (GET)
* Gérer les emprunts de livres :
 + Emprunter un livre : `/livres/{id}/emprunts` (POST)
 + Rendre un livre : `/livres/{id}/emprunts/{idEmprunt}` (DELETE)
* Authentification :
 + Se connecter : `/authentification` (POST)
 + Se déconnecter : `/authentification` (DELETE)

## Architecture

* Base de données : PostgreSQL
* Framework : Spring Boot
* Bibliothèque de validation : Hibernate Validator
* Bibliothèque de tests : JUnit 5
* Bibliothèque de documentation : Swagger/OpenAPI

## Exécution

1. Cloner ce projet à l'aide de Git.
2. Exécuter la commande `mvn spring-boot:run` pour démarrer l'application.
3. Accéder à l'application à l'adresse `http://localhost:8080`.

## Documentation

* Swagger/OpenAPI : `http://localhost:8080/swagger-ui.html`
* Javadoc : `http://localhost:8080/javadoc`

## Tests

* Tests unitaires : `mvn test`

## Validation des données

* Validation des données effectuée à l'aide de Hibernate Validator.

## Gestion des erreurs

* Gestion des erreurs effectuée à l'aide de Spring Boot.

## Auteur

* Auteur : Votre nom
* Email : Votre email

## Licence

* Licence : Apache License 2.0
