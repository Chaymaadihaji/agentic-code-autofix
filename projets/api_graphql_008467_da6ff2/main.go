go
// main.go

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/graph-gophers/golang-gqlgen/graphql/handler"
	"github.com/graph-gophers/golang-gqlgen/graphql/handler/extension"
	"github.com/graph-gophers/golang-gqlgen/graphql/playground"
	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"github.com/lib/pq"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

var err error

const port = "8080"
const jwtSecret = "jwtsecret"
const dbUser = "postgres"
const dbPassword = "password"
const dbHost = "localhost"
const dbPort = "5432"
const dbName = "database"

func init() {
	// Load .env
	if err := godotenv.Load(); err != nil {
		log.Fatal(err)
	}

	// Get environment variables
	jwtSecret = os.Getenv("JWT_SECRET")
	dbUser = os.Getenv("DB_USER")
	dbPassword = os.Getenv("DB_PASSWORD")
	dbHost = os.Getenv("DB_HOST")
	dbPort = os.Getenv("DB_PORT")
	dbName = os.Getenv("DB_NAME")
}

type Resolver struct{}

func (r *Resolver) Mutation() MutationResolver {
	return &mutationResolver{r}
}

func (r *Resolver) Query() QueryResolver {
	return &queryResolver{r}
}

func (r *Resolver) Subscription() SubscriptionResolver {
	return &subscriptionResolver{r}
}

func runDatabaseSchema() {
	pg := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s",
		dbHost, dbPort, dbUser, dbPassword, dbName,
	)

	_, err := pq.ParseConfig(pg)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	// Gqlgen
	mgr := NewGQLOperationManager()

	typeQuery, err := LoadSchema(&Resolver{})
	if err != nil {
		log.Fatal(err)
	}

	cfg := handler.Config{
		Schema:                    typeQuery,
		Prefetch:                   true,
		AutoCompletions:            nil,
		DisableIntroscription:      false,
		Playground:                 playground.Config{GraphQLAPI: &playground.API{Title: "GraphQL API"}},
		Extensions:                 []extension.Extension{extension.Introspection, graphqlDebugging},
		Middleware:                 nil,
		DisableErrorpplications:    false,
	}

	s := handler.New(cfg)

	typeGraphQL = *typeQuery.Schema().(*graph.graphSchema)

	s.AddInterceptor(func(next handler.FieldInterceptor) handler.FieldInterceptor {
		return func(ctx context.Context, fn handler.FieldResolveF) (interface{}, error) {
			// Do something before resolving the field
			return fn(ctx)
		}
	})

	// Base de données
	runDatabaseSchema()

	// Echo
	e := echo.New()

	greeting := func(c echo.Context) error {
		name := c.Param("name")
		return c.String(http.StatusOK, "Hello, "+name+"!")
	}

	// Authentication
	e.Use(authJWT())
	e.Use(middleware.CORS())
	e.GET("/graphql", graphqlHandler(s))
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello World - API GraphQL avec JWT")
	})

	if err := e.Start(":" + port); err != nil {
		log.Fatal(err)
	}
}
