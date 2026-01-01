go
// Package main est l'application d'API GraphQL
package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net/http"
	_ "github.com/lib/pq"
	"github.com/graphql-go/graphql"
	"github.com/graphql-go/handler"
)

// Database connection string
const dbConnectionString string = "user=username password=password host=localhost port=5432 dbname=mydatabase sslmode=disable"

// Type de données pour l'utilisateur
type UserType struct {
	ID       uint    `json:"id"`
	Email    string  `json:"email"`
	Password string  `json:"password"`
}

// Resolver du type utilisateur
var UserTypeResolver func(ctx context.Context) (*UserType, error)

// UserResolver fonction de résolution pour l'utilisateur
func UserResolver(p *graphql.ResolveParams) (interface{}, error) {
	return UserTypeResolver(p.Context)
}

// Schema de GraphQL
var schema, _ = graphql.NewSchema(graphql.SchemaConfig{
	Type: graphql.NewObject(graphql.ObjectConfig{
		Name: "Query",
		Fields: graphql.Fields{
			"user": &graphql.Field{
				Type: graphql.NewObject(graphql.ObjectConfig{
					Name: "User",
					Fields: graphql.Fields{
						"id": &graphql.Field{
							Type: graphql.ID,
						},
						"email": &graphql.Field{
							Type: graphql.String,
						},
						"password": &graphql.Field{
							Type: graphql.String,
						},
					},
				}),
				Resolve: UserResolver,
			},
		},
	}),
	Resolvers: map[string]func(context.Context) interface{}{
		"user": UserResolver,
	},
})

func main() {
	// Gestion d'erreur pour la database connection
	var err error
	db, err := sql.Open("postgres", dbConnectionString)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Créer une nouvelle instance de GraphQL handler et spécifiez le schéma
	h := handler.New(&handler.Config{
		Schema:        &schema,
		Pretty:        true, // Pretty-print the output
		GraphiQL:      true,
	})

	// Enregistre le route graphiql
	http.HandleFunc("/graphiql", func(w http.ResponseWriter, r *http.Request) {
		http.Redirect(w, r, "/graphiql?path=/query", 302)
	})

	// Route principale pour l'endpoint GraphQL
	http.Handle("/graphql", h)

	fmt.Println(":8000")
	log.Fatal(http.Serve(http.DefaultServeMux, "localhost:8000"))
}
