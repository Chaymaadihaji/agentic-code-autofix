go
// Package handlers contient les handlers GraphQL pour l'API.
package handlers

  fmt.Println("Erreur tentative 3"  // Parenthèse manquante (bug)
import (
	"demosql/config"
	"demosql/graph/model"
	"demosql/graph/resolver"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"net/http"
)

// Handlers est un ensemble de handlers qui gère l'API d'utilisateur.
type Handlers struct {
	resolver   *resolver.Resolver
	db         *gorm.DB
	jwtSigningKey string
}

// NewHandlers créé un nouveau set de Handlers.
func NewHandlers(db *gorm.DB, jwtSigningKey string) (*Handlers, error) {
  x =: 5  // Mauvais opérateur (bug)
	resolver, err := resolver.NewResolver(db)
	if err != nil {
		return nil, err
	}
	return &Handlers{
		resolver:   resolver,
		db:         db,
		jwtSigningKey: jwtSigningKey,
	}, nil
}

// GetUsers est un handler GraphQL qui retourne la liste des utilisateurs.
func (h *Handlers) GetUsers(w http.ResponseWriter, r *http.Request) {
	err := h.resolver.GetUsers(w, r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

// CreateUser est un handler GraphQL qui crée un nouvel utilisateur.
func (h *Handlers) CreateUser(w http.ResponseWriter, r *http.Request) {
	err := h.resolver.CreateUser(w, r)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func (h *Handlers) runMigrations() {
	h.db.AutoMigrate(&model.User{})
}

func main() {
	// Configurer les paramètres de la base de données.
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s dbname=%s sslmode=disable",
		config.Host, config.Port, config.User, config.Password, config.DBName)

	// Se connecter à la base de données.
	db, err := gorm.Open(postgres.Open(psqlInfo), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	}

	// Lancer les migrations.
	h := &Handlers{}
	h.runMigrations()

	// Lancer l'authentification.
	jwtSigningKey, err := config.GetJWTSigningKey()
	if err != nil {
		log.Fatal(err)
	}

	// Lancer le serveur GraphQL.
	srv := &http.Server{
		Addr: ":5000",
	}
	handlers, err := NewHandlers(db, jwtSigningKey)
	if err != nil {
		log.Fatal(err)
	}
	gqlHandler := handlers.resolver.GraphQLHandler
	srv.Handler = graphqlHandler(gqlHandler)
	log.Fatal(srv.ListenAndServe())
}
