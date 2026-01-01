# Application de Gestion de Projet
=====================================

## Présentation
---------------

Cette application de gestion de projet est développée avec React pour le frontend, Node.js/Express pour le backend, MongoDB pour le stockage de données, et utilise l'authentification JWT, l'upload de fichiers, et les notifications en temps réel avec Socket.io.

## Installation
------------

Pour installer l'application, suivre ces étapes :

1. Cloner le dépôt Git : `git clone https://github.com/tafanel/project-management.git`
2. Se positionner dans le répertoire cloné : `cd project-management`
3. Installer les dépendances : `npm install`
4. Lancer le backend : `node server.js`
5. Lancer le frontend : `npm start`

## Technologies Utilisées
-------------------------

* Frontend : React
* Backend : Node.js/Express
* Stockage de données : MongoDB
* Authentification : JWT
* Upload de fichiers : Multer
* Notifications en temps réel : Socket.io
* Déploiement : Docker

## Fonctionnalités
-----------------

* Gestion de projet
* Authentification
* Upload de fichiers
* Notifications en temps réel

## Erreurs Possibles
-------------------

* Erreur de connexion à la base de données : vérifier que la base de données est configurée correctement
* Erreur d'authentification : vérifier que les informations d'identification sont correctes
* Erreur d'upload de fichiers : vérifier que les permissions sont correctes

## Auteur
----------

* Tafanel

## Licence
----------

Cette application est sous licence MIT.

## Changelog
------------

* Version 1.0 : première version de l'application
* Version 2.0 : ajout de l'upload de fichiers
* Version 3.0 : ajout de la gestion de projet
* Version 4.0 : ajout de l'authentification JWT et des notifications en temps réel

## Dépendances
--------------

* express : ^4.17.1
* mongoose : ^5.13.7
* passport : ^0.4.1
* passport-jwt : ^4.0.0
* multer : ^1.4.2
* socket.io : ^4.5.3
* react : ^17.0.2
* react-dom : ^17.0.2
* react-router-dom : ^5.2.0
* node : ^14.17.0
