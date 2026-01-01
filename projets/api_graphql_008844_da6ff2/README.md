markdown
# API GraphQL avec Go et PostgreSQL

## Table des matières

* [Description](#description)
* [Concessions Techniques](#requis-techniques)
* [Utilisation](#utilisation)
* [Dépendances](#dépendances)
* [Installation](#installation)
* [Execution](#execution)
* [Tests](#tests)
* [Erreurs Possibles](#erreurs-possibles)

## Description

Cette API GraphQL est développée avec Go et utilise Gqlgen pour la génération d'API. Elle utilise également PostgreSQL pour la base de données et JWT pour l'authentification.

## Concessions Techniques

* Langage principal: Go
* Type de base de données: PostgreSQL
* Bibliothèque GraphQL: Gqlgen
* Méthode d'authentification: JWT

## Utilisation

L'API est utilisée pour interactuer avec la base de données PostgreSQL. Elle fournit des endpoints pour créer, lire, mettre à jour et supprimer des ressources.

## Dépendances

Pour mettre en œuvre ce projet, les suivants sont nécessaires :
- Go (version 1.17 ou supérieure)
- GolangCI-Lint (pour l'analyse de code)
- Glide (pour la gestion de dépendances)
- PostgreSQL (dans la version 12 ou supérieure)

## Installation

1. Clonez ce dépôt git.
2. Configurez votre projet pour faire référence au fichier ``glide.yaml``.
3. Tirez les dépendances nécessaires en exécutant la commande suivante :
