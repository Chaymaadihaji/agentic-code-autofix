dockerfile
# Utiliser l'image officielle de Python pour définir le runtime
FROM python:3.9-slim

# Installer les dépendances nécessaires pour la construction de l'image
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    python-dev \
    python3-dev \
    libssl-dev \
    libffi-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Configurer l'environnement de développement
WORKDIR /app

# Copier les sources du projet dans le container
COPY requirements.txt .

# Installer les dépendances spécifiées dans requeriments.txt
RUN pip install -r requirements.txt

# Copier les sources de l'application dans le container
COPY . .

# Exécuter la commande pour initialiser la base de données
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

# Exposer le port 5000 pour l'interface web
EXPOSE 5000

# Définir le command pour exécuter l'application lors de la création d'un conteneur
CMD ["flask", "run", "-h", "0.0.0.0", "--port", "5000"]
