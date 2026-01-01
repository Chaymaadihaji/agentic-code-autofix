go
// models/models.go

package models

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/lib/pq"

	"github.com/graphql-go/graphql"
	"github.com/graphql-go/graphql/gqlerrors"
	"github.com/graphql-go/relay"
	"github.com/graph-gophers/graphql-go/relay/connection"
	"github.com/graph-gophers/graphql-koa/kit"

	"github.com/dgrijalva/jwt-go"
)

// TypeUser represent an user
type TypeUser struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Email   string `json:"email"`
	Password string `json:"password"`
}

// UserType define an user type
var UserType = graphql.NewObject(graphql.ObjectConfig{
	Name: "User",
	Fields: graphql.Fields{
		"id": &graphql.Field{
			Type: graphql.String,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeUser).ID, nil
			},
		},
		"name": &graphql.Field{
			Type: graphql.String,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeUser).Name, nil
			},
		},
		"email": &graphql.Field{
			Type: graphql.String,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeUser).Email, nil
			},
		},
		"password": &graphql.Field{
			Type: graphql.String,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeUser).Password, nil
			},
		},
	},
})

// TypeBook represent a book
type TypeBook struct {
	ID       string `json:"id"`
	Title    string `json:"title"`
	Author   string `json:"author"`
	Pages    int    `json:"pages"`
	Price    float64 `json:"price"`
	Released time.Time `json:"released"`
}

// TypeBookEdge represent an edge for a book connection
type TypeBookEdge struct {
	relay.EdgeField

	Node    *TypeBook    `json:"node"`
	Cursor  string       `json:"cursor"`
}

// TypeBookConnection represent a connection for books
type TypeBookConnection struct {
	relay.Connection
	Edges []TypeBookEdge `json:"edges"`
}

// TypeBookType defines the book type
var TypeBookType = graphql.NewObject(graphql.ObjectConfig{
	Name: "Book",
	Fields: graphql.Fields{
		"id": &graphql.Field{
			Type: graphql.String,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeBook).ID, nil
			},
		},
		"title": &graphql.Field{
			Type: graphql.String,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeBook).Title, nil
			},
		},
		"author": &graphql.Field{
			Type: graphql.String,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeBook).Author, nil
			},
		},
		"pages": &graphql.Field{
			Type: graphql.Int,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeBook).Pages, nil
			},
		},
		"price": &graphql.Field{
			Type: graphql.Float,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeBook).Price, nil
			},
		},
		"released": &graphql.Field{
			Type: graphql.DateTime,
			Resolve: func(obj interface{}) (interface{}, error) {
				return obj.(*TypeBook).Released, nil
			},
		},
	},
})

// GraphQLType returns the GraphQL schema type
func GraphQLType(schema *graphql.Schema) graphql.Object {
	return graphql.NewObject(graphql.ObjectConfig{
		Name: "GraphQL",
		Fields: graphql.Fields{
			"books": &graphql.Field{
				Type: connection.NewPageResolver(connection.PageOptions{
					EdgeType:            TypeBookEdge{},
					EdgeToNodeResolver: func(e interface{}) (interface{}, error) {
						return e.(*TypeBookEdge).Node, nil
					},
					NodeType: TypeBookType,
				}),
				Resolve: func(obj interface{}) (interface{}, error) {
					return connection.GetNodes(s, nil), nil
				},
			},
		},
	})
}

// DB represent a PostgreSQL database connection
type DB struct {
	SQL *sql.DB
}

// DBConn return a connection instance
func DBConn() (*DB, error) {
	SQL, err := sql.Open("postgres", "user=root password=passwd dbname=graphql sslmode=disable")
	return &DB{SQL: SQL}, err
}

// DBInit perform database initialization
func DBInit(ctx context.Context, db *DB) error {
	_, err := db.SQL.ExecContext(ctx, `
		CREATE TABLE IF NOT EXISTS users (
			id serial PRIMARY KEY,
			name VARCHAR(255) NOT NULL,
			email VARCHAR(255) NOT NULL,
			password VARCHAR(255) NOT NULL
		);
		CREATE TABLE IF NOT EXISTS books (
			id serial PRIMARY KEY,
			title VARCHAR(255) NOT NULL,
			author VARCHAR(255) NOT NULL,
			pages INTEGER NOT NULL,
			price FLOAT NOT NULL,
			released TIMESTAMP NOT NULL
		);
	`)
	return err
}

// Authenticate verify user identity
func Authenticate(ctx context.Context, db *DB, email, password string) (*TypeUser, error) {
	var user TypeUser
	err := db.SQL.QueryRowContext(ctx, `SELECT * FROM users WHERE email=$1 AND password=$2`, email, password).Scan(&user.ID, &user.Name, &user.Email, &user.Password)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, gqlerrors.ErrorWrap(fmt.Errorf("authenticaton failed"), "invalid email and password combination")
		}
		log.Println(err)
		return nil, fmt.Errorf("database error")
	}
	return &user, nil
}

// JWTGenerate generate a JWT token for authentication
func JWTGenerate(user *TypeUser) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": user.ID,
	})
	return token.SignedString([]byte(os.Getenv("JWT_KEY")))
}

// JWTVerify verify a JWT token
func JWTVerify(token string) (*jwt.Token, error) {
	return jwt.Parse(token, func(token *jwt.Token) (interface{}, error) {
		return []byte(os.Getenv("JWT_KEY")), nil
	})
}

// WSHandle WebSocket connection handler
func WSHandle(ws *websocket.Conn) {
	log.Println("new client connected")
	defer ws.Close()

	// Handle incoming messages
	for {
		_, message, err := ws.ReadMessage()
		if err != nil {
			break
		}
		// Handle outgoing messages
		err = ws.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			break
		}
	}
}
