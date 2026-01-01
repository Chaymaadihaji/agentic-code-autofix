bash
# Installer les dépendances
go get -u github.com/graphql/golang/graphql
go get -u github.com/graphql-go/graphql-go
go get -u github.com/99designs/gqlgen
go get -u gopkg.in/yaml.v3
go get -u github.com/lib/pq

# Configurer les variables d'environnement
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=myuser
export DB_PASSWORD=mypass
export JWT_SECRET=mysecret
