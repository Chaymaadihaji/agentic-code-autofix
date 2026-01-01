markdown
# API REST de Sécurité avancée avec Spring Boot

## Présentation
API REST sécurisée pour la gestion des utilisateurs et des rôles, développée en utilisant Spring Boot avec Spring Security et PostgreSQL.

## Fonctionnalités

### Sécurité
- Authentification via token JWT
- Autorisation basée sur les rôles

### API REST
- Gestion des utilisateurs (inscription, connexion, mise à jour, suppression)
- Gestion des rôles (ajout, mise à jour, suppression)

### Performances
- Optimisation des requêtes pour améliorer les performances

## Utilisation

### Installation
- Cloner le projet avec le code `git clone https://github.com/tonprojet/api-rest-spring-boot.git`
- Exécuter la commande `mvn clean install`
- Lancer le projet avec le code `mvn spring-boot:run`

### Déploiement
- Les instructions de déploiement Docker peuvent être trouvé dans le fichier [Dockefile](https://github.com/tonprojet/api-rest-spring-boot/blob/main/Dockerfile)

## Tests unitaires
Les tests unitaires ont été exécutés avec succès au moyen d'[JUnit 5](https://junit.org/junit5/)

## Documentation
-La documentation API a été générée au moyen de [Swagger OpenAPI](https://swagger.io/specification/)
-Pour vous y faire accéder : `http://localhost:8080/swagger-ui/index.html`
