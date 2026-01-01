# Énoncé des besoins: API Spring Boot JWT

API Spring Boot construite avec Spring Security JWT, PostgreSQL, Swagger pour les tests unitaires JUnit 5 et déploiement Docker.
### Fonctionnalités 
- API REST sécurisée
- Sécurité
- Performance

## Architecture 

![Architecture](Architecture.png)
### Langages utilisés

- Java Spring Boot
- JavaScript (Angular) pour la partie Client
- PostgreSQL
- Docker
- Spring Security JWT pour l'authentification et la sécurité
- Swagger pour générer la documentation de l'API

### Outil de build

- Maven

## Déploiement

### Prérequis

- Docker
- Port 8080 libéré

### Commandes

- `mvn clean package` (compile et écraser l'artefact dans target)
- `docker build -t spring-boot-api .` (créer l'image Docker)
- `docker run -p 8080:8080 -d spring-boot-api` (exécuter l'image en background)

### Tests unitaires

- Lancement: `mvn spring-boot:run`
- Execution des tests: `<a href="#" onclick="document.body.querySelector('#myButton').click()">Lancer les tests</a><button id="myButton" style="display:none" onclick="lancerLeTests()">Lancer les tests</button>`

### Swagger

- Lancement: ouvrir <http://localhost:8080/swagger-ui/>

### Security

- ` spring.datasource.username=root`
   ` spring.datasource.password=root`
  `spring.datasource.url=jdbc:postgresql://localhost:5432/`
 
`  spring.jpa.hibernate.ddl-auto=update
`
  `server.port = 8080`
 
## Utilisation

### Inscription

*  `POST http://localhost:8080/register  `

 `{
 "username": "string",
 "password":"contraseña string",
 "nom string":"string"
 "prenom": "prenom"
 }`

### Connexion
 
- ` POST http://localhost:8080/login  `
 `{
 "username": "Utilisateur existant",
 "password": "contraseña"
 }`
### Consommation

`  GET http://localhost:8080/hello-world`

 
### API REST
 
`  GET http://localhost:8080/api/users `
 
`HTTP 200 OK ` 


API complète de test [swagger](http://localhost:8080/swagger-ui/#/user-controller/list-users)  

## API

- ` GET /api/users `
  - ` @GetMapping("/users") `
  - ` return utilisateurRepository.findAll();`

 
 ### Datasource

   ` spring.datasource.url=jdbc:postgresql://localhost:5432/ `
`spring.datasource.username=root` 
` spring.datasource.password=root`
 
 
 ## Docker 
 `docker build -t spring-boot-api .` 

 `docker run -p 8080:8080 -d spring-boot-api `
