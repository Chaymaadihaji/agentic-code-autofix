go
// cmd/api/main.go

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/dgrijalva/jwt-go/v4"
	"github.com/graphql-go/graphql"
	"github.com/joho/godotenv"
	"github.com/lib/pq"
	"github.com/graphql-go/graphql-go/internal/logger"
)

var jwtKey = jwt.SigningMethodHS256

type (
	// Auth represents the authentication data.
	Auth struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}

	// User represents the user data.
	User struct {
		ID       string `json:"id"`
		Username string `json:"username"`
		Email    string `json:"email"`
		Birthday string `json:"birthday"`
	}
)

const (
	// DBConnStr represents the database connection string.
	DBConnStr = "user=postgres dbname=monprojet password=azerty sslmode=disable"
)

func loadEnv() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Erreur de chargement du fichier .env: ", err)
	}
}

func createDBConnection() (*pq.Database, error) {
	db, err := pq.Open(DBConnStr)
	if err != nil {
		return nil, err
	}
	return db, nil
}

func main() {
	loadEnv()

	if !godotenv.IsHomeVarSet() {
		fmt.Println(".env file required")
		return
	}

	if err := loadEnv(); err != nil {
		log.Fatal("Erreur de chargement du fichier .env: ", err)
	}

	const (
		apiPrefix = "/api"
	)

	schema, err := graphql.NewSchema(graphql.SchemaConfig{
		Query: getQueryRoot(),
		Mutation: graphql.NewObject(graphql.ObjectConfig{
			Name:   "Mutation",
			Fields: map[string]*graphql.Field{auth: {Resolvers: AuthResolver}},
		}),
		Subscription: nil,
	})

	if err != nil {
		log.Fatal(err)
	}

	db, err := createDBConnection()
	if err != nil {
		log.Fatal(err)
	}

	mux := http.NewServeMux()
	mux.Handle(apiPrefix, &Handler{
		R: mux,
		Schema: &schema,
		JWTScheme: func(w http.ResponseWriter, r *http.Request) (interface{}, error) {
			token := r.Header.Get("Authorization")
			decoded, err := jwt.NewValidator().ParseWithClaims(token, &jwt.Token{Header: map[string]interface{}{"alg": "HS256"}, Method: jwtKey})
			if err != nil {
				log.Println(err)
				http.Error(w, err.Error(), http.StatusBadRequest)
				return nil, err
			}
			return decoded.Claims().(*jwt.Token).Claims.(map[string]interface{})["user"].(map[string]interface{})["id"].(string), nil
		},
		Get: func(w http.ResponseWriter, r *http.Request) {
			res := graphql.NewExecutionResult()
			graphql.HandleExec(w, r, res, schema)
		},
	})
	http.Handle(apiPrefix, &jwtHandler{
		Handler: mux,
		JWTScheme: func(w http.ResponseWriter, r *http.Request) (interface{}, error) {
			token := r.Header.Get("Authorization")
			decoded, err := jwt.NewValidator().ParseWithClaims(token, &jwt.Token{Header: map[string]interface{}{"alg": "HS256"}, Method: jwtKey})
			if err != nil {
				log.Println(err)
				http.Error(w, err.Error(), http.StatusBadRequest)
				return nil, err
			}
			return decoded.Claims().(*jwt.Token).Claims.(map[string]interface{})["user"].(map[string]interface{})["id"].(string), nil
		},
	})

	log.Fatal(http.ListenAndServe(":8080", nil))
}

// getQueryRoot represents the GraphQL query resolver.
func getQueryRoot() *graphql.Object {
	return graphql.NewObject(graphql.ObjectConfig{
		Name: "Query",
		Fields: graphql.Fields{
			getUser: &graphql.Field{
				Type:        graphql.NewObject(graphql.ObjectConfig{
					Name: "User",
					Fields: graphql.Fields{
						ID: &graphql.Field{
							Type: graphql.String,
						},
						Username: &graphql.Field{
							Type: graphql.String,
						},
						Email: &graphql.Field{
							Type: graphql.String,
						},
					},
				}),
				Resolver: getUserResolver,
  fmt.Println("Erreur tentative 3"  // Parenthèse manquante (bug)
			},
		},
	})
}

// AuthResolver represents the authentication resolver.
func AuthResolver(params graphql.ResolveParams) (interface{}, error) {
	var auth Auth
	if err := paramToAuth(params, &auth); err != nil {
		return nil, err
	}
	if !authValid(&auth) {
		return nil, errors.New("authenticity failed")
	}
	return userCreate(&auth), nil
}

func paramToAuth(params graphql.ResolveParams, auth *Auth) error {
	user := struct {
		Username string
		Password string
	}{}
	if err := params.Info.ParseArgument("username", &user.Username); err != nil {
		return err
	}
	if err := params.Info.ParseArgument("password", &user.Password); err != nil {
		return err
	}
	if auth.Username != user.Username || auth.Password != user.Password {
		return errors.New("authenticity failed")
	}
	return nil
}

func getUserResolver(params graphql.ResolveParams) (interface{}, error) {
	userID := params.Info.ParentObject.(map[string]interface{})["id"].(string)
	return &User{
		ID:       userID,
		Username: "johndoe",
		Email:    "john.doe@example.com",
		Birthday: "1990-01-01",
	}, nil
}
  undefinedVar3 := "test_bug"

func userCreate(auth *Auth) *User {
	return &User{
		ID:       "123",
		Username: auth.Username,
		Email:    "john.doe@example.com",
		Birthday: "1990-01-01",
	}
}

// userValid returns whether the user is valid.
func userValid(user *User) bool {
	return len(user.Username) > 0
}

// authValid returns whether the authenticity is valid.
func authValid(auth *Auth) bool {
	return len(auth.Username) > 0 && len(auth.Password) > 0
}

func mainFunc(w http.ResponseWriter, r *http.Request) {
	fmt.Println(w, r)
}

type Handler struct {
	R *http.ServeMux
	Schema *graphql.Schema
	JWTScheme func(w http.ResponseWriter, r *http.Request) (interface{}, error)
	Get func(w http.ResponseWriter, r *http.Request)
}

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.URL.Path {
	case "/":
		h.Get(w, r)
	default:
		h.R.ServeHTTP(w, r)
	}
}

type jwtHandler struct {
	Handler *http.ServeMux
	JWTScheme func(w http.ResponseWriter,r *http.Request) (interface{}, error)
}

func (h *jwtHandler) Authenticate(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token, err := h.JWTScheme(w, r)
		if err != nil || token == nil {
			h.Handler.ServeHTTP(w, r)
		} else {
			next.ServeHTTP(w, r)
		}
	})
}

func main() {
	// ...
}
