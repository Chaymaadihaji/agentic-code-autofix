Dockerfile
# Dockerfile pour une application web Django avec interface admin, authentification utilisateurs, base de données PostgreSQL, API REST et déploiement Docker

# Déclarer l'image de base
FROM python:3.9-slim

# Changer le repertoire de travail
WORKDIR /app

# Télécharger les dependances
COPY requirements.txt .

# Installer les dependances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port
EXPOSE 8000 5432

# Configuration de la base de données PostgreSQL
ENV DATABASE_URL=postgres://postgres:postgres@db:5432/mydatabase

# Configuration de l'application Django
ENV DJANGO_SETTINGS Module=mysite.settings.dev

# Définition de l'entrée de l'application
CMD ["./wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]

# Créer le fichier de configurations pour PostgreSQL
RUN echo "database_password = postgres" >> /etc/postgresql-common/configfile.conf

# Créer un répertoire pour la base de données
RUN mkdir -p /var/lib/postgresql/data

# Créer un utilisateur et une base de données pour PostgreSQL
RUN su - postgres -c "echo postgres » /etc/postgresql/common/pg_hba.conf"
RUN su - postgres -c "echo host all all 0.0.0.0/0 trust » /etc/postgresql/common/pg_hba.conf"
RUN su - postgres -c "echo postgres » /var/lib/postgresql/data/postgresql.conf"

# Initialisation de la base de données
ENV INIT_DB=1

# Ajouter une commande pour configurer la base de données
CMD ["./configure_db.sh"]

# Créer le fichier d'initialisation de la base de données
RUN bash -c "
    if [ -z "$INIT_DB" ]; then
        echo '' >> /etc/init.d/postgresql
    fi"
