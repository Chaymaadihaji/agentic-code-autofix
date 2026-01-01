bash
# docker-compose.yml

version: '3'
services:
  api_gateway:
    build: ./api_gateway
    ports:
      - "80:80"
    depends_on:
      - service_produits
      - service_utilisateurs
      - service_commandes
      - service_paiement
      - service_notification

  service_produits:
    build: ./service_produits
    ports:
      - "5000:5000"
    depends_on:
      - db

  service_utilisateurs:
    build: ./service_utilisateurs
    ports:
      - "5001:5001"
    depends_on:
      - db

  service_commandes:
    build: ./service_commandes
    ports:
      - "5002:5002"
    depends_on:
      - redis

  service_paiement:
    build: ./service_paiement
    ports:
      - "5003:5003"

  service_notification:
    build: ./service_notification
    ports:
      - "5004:5004"

  db:
    image: postgres
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=mydb

  redis:
    image: redis
