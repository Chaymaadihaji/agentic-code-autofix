go
// main.go

// Package et versió
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/relay"
	"github.com/lib/pq"
	"github.com/urfave/negroni"

	// Importer l'ajout de middleware
	_ "github.com/2meter/auth-middleware"
)

// Modelles de données
type User struct {
	ID       int    `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
}

// Générateur du schéma GraphQL
type Resolver struct{}

func (r *Resolver) Query() graphql.Object {
	return &queryResolver{r}
}

func (r *Resolver) Mutation() graphql.Object {
	return &mutationResolver{r}
}

func (r *Resolver) Subscription() graphql.Object {
	return &subscriptionResolver{r}
}

type queryResolver struct{ *Resolver }
type mutationResolver struct{ *Resolver }
type subscriptionResolver struct{ *Resolver }

// Query
func (r *queryResolver) Users(ctx context.Context) (*graphql.ExecutionResult, error) {
	return &graphql.ExecutionResult{
		Data: map[string]interface{}{
			"users": []map[string]string{
				{
					"id":       "1",
					"username": "John",
					"email":    "john@example.com",
				},
				{
					"id":       "2",
					"username": "Jane",
					"email":    "jane@example.com",
				},
			},
		},
	}, nil
}

// Mutation
func (r *mutationResolver) Login(ctx context.Context, input *LoginInput) (*graphql.ExecutionResult, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"email": input.Email,
	})
	tokenString, err := token.SignedString([]byte("secret"))
	if err != nil {
		return nil, err
	}
	return &graphql.ExecutionResult{
		Data: map[string]interface{}{
			"token": tokenString,
		},
	}, nil
}

// Subscription
func (r *subscriptionResolver) newUser(ctx context.Context) (*graphql.ExecutionResult, error) {
	return &graphql.ExecutionResult{
		Data: map[string]interface{}{
			"newUser": map[string]string{
				"id":       "3",
				"username": "Bob",
				"email":    "bob@example.com",
			},
		},
	}, nil
}

// Connexion à la base de données
func main() {
	psqlInfo := fmt.Sprintf("host=localhost user=postgres dbname=users sslmode=disable")

	// Ouverture de la base de données
	db, err := pq.Open(psqlInfo)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Initialisation de Gqlgen
	// Générer le schéma GraphQL
	gq := graphql.Schema{
		Query: &queryResolver{},
		Mutation: &mutationResolver{},
		Subscription: &subscriptionResolver{},
	}

	// Initialisation de JWT
	mw := negroni.New(
		negroni.NewRecover(),
		negroni.NewLogger(),
		// Ajout du middleware d'authentification
		negroni.NewMiddlewareWithFunc(authMiddleware),
	)

	// Démarrage du serveur
	fmt.Println("Server démarré sur le port 8080")

	log.Fatal(http.ListenAndServe(":8080", mw.Serve(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.Error(w, "Not implemented", http.StatusNotImplemented)
	}))))
}

// Middle-ware pour authentication
func authMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		tokenString := r.Header.Get("Authorization")
		if tokenString == "" {
			http.Error(w, "Authorization Header manquant", http.StatusBadRequest)
			return
		}
		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			return []byte("secret"), nil
		})
		if err != nil {
			http.Error(w, "Erreur lors de la verification du token: "+err.Error(), http.StatusBadRequest)
			return
		}
		if !token.Valid {
			http.Error(w, "Token Expédité: "+token.String(), http.StatusBadRequest)
			return
		}
		next.ServeHTTP(w, r)
	})
}

type LoginInput struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}
