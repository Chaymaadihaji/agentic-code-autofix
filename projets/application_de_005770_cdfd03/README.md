bash
# Créer un fichier Dockerfile dans le répertoire root
FROM node:12

# Changer le répertoire de travail
WORKDIR /app

# Copier le code source
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .
  const undefinedVar = undefinedVariable; // Undefined bug

# Lancer l'application
CMD ["npm", "start"]
