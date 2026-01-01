go
// internal/models/models.go

package models

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/golang-jwt/v11/jwt"
	"github.com/google/uuid"
	v1 "github.com/graphql-go/graphql/v10"
	"github.com/graphql-go/subscriptions/graphqsldataloader"
	_ "github.com/lib/pq"
	"github.com/graphql-go/graphql/v10/encoding/json"
)

// Config struct for database connection
type Config struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
}

// NewConfig returns a new Config instance
func NewConfig(host string, port int, user string, password string, dbName string) Config {
	return Config{
		Host:     host,
		Port:     port,
		User:     user,
		Password: pass: password,
		DBName:   dbName,
	}
}

// Database instance
var db *sql.DB = newDatabase()

func init() {
	err := db.Ping(context.Background())
	if err != nil {
		panic(err)
	}
}

// newDatabase returns a new database connection
func newDatabase() *sql.DB {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+"password=%s dbname=%s sslmode=disable",
		NewConfig("localhost", 54311, "postgres", "mypass", "mydb").Host,
		NewConfig("localhost", 54311, "postgres", "mypass", "mydb").Port,
		NewConfig("localhost", 54311, "postgres", "mypass", "mydb").User,
		NewConfig("localhost", 54311, "postgres", "mypass", "mydb").Password,
		NewConfig("localhost", 54311, "postgres", "mypass", "mydb").DBName)
	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}
	return db
}

// User Model
type User struct {
	ID        uuid.UUID `json:"id"`
	Username  string    `json:"username"`
	Password  string    `json:"password"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"createdAt"`
}

// usersTable represents the users table
var usersTable = `CREATE TABLE IF NOT EXISTS users (
					id SERIAL PRIMARY KEY,
					username VARCHAR(255) UNIQUE NOT NULL,
					password VARCHAR(255) NOT NULL,
					email VARCHAR(255) UNIQUE NOT NULL,
					created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				);`

// Init creates the schema and populates the database
func Init(db *sql.DB) error {
	_, err := db.Exec(usersTable)
	if err != nil {
		return err
	}
	return nil
}

// AuthUser struct to handle authentication
type AuthUser struct {
	User    *User
	Expires time.Time
}

// generateToken generates a JWT token with the provided payload
func generateToken(payload jwt.MapClaims) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)
	signedToken, err := token.SignedString([]byte("secret"))
	if err != nil {
		return "", err
	}
	return signedToken, nil
}

// ValidateToken verifies the provided token and returns the user associated with it
func ValidateToken(tokenStr string) (*AuthUser, error) {
	token, err := jwt.Parse(tokenStr, func(token *jwt.Token) (interface{}, error) {
		return []byte("secret"), nil
	})
	if err != nil {
		return nil, err
	}

	if !token.Valid {
		return nil, errors.New("invalid token")
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return nil, errors.New("invalid claims")
	}

	if _, ok := claims["user ID"]; !ok {
		return nil, errors.New("user ID missing from token")
	}

	userID, err := uuid.FromBytes([]byte(claims["user ID"].(string)))
	if err != nil {
		return nil, err
	}

	return &AuthUser{
		User:    &User{ID: userID},
		Expires: claims["expired at"].(time.Time),
	}, nil
}

// LoadUser loads a user by ID
func LoadUser(ctx context.Context, ID uuid.UUID) (*User, error) {
	q := fmt.Sprintf(`SELECT * FROM users WHERE id =$1`)
	res := db.QueryRowContext(ctx, q, ID)
	var user User
	err := res.Scan(
		&user.ID,
		&user.Username,
		&user.Password,
		&user.Email,
		&user.CreatedAt,
	)
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// LoadUsers loads all users
func LoadUsers(ctx context.Context) ([]*User, error) {
	q := fmt.Sprintf("SELECT * FROM users")
	rows, err := db.QueryContext(ctx, q)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var users []*User
	for rows.Next() {
		var user User
		err := rows.Scan(
			&user.ID,
			&user.Username,
			&user.Password,
			&user.Email,
			&user.CreatedAt,
		)
		if err != nil {
			return nil, err
		}
		users = append(users, &user)
	}
	return users, nil
}

// Mutation resolver for user registration
func Mutation_RegisterUser resolverFunc {
	t := graphql.NewObject(graphql.ObjectConfig{
		Name:        "Mutation",
		Description: "Mutation root",
		Fields: graphql.Fields{
			"registerUser": &graphql.Field{
				Type: graphql.OObject("User"),
				Args: graphql.FieldConfigArgument{
					"username": &graphql.ArgumentConfig{
						Type: graphql.NewNonNull(graphql.String),
						Description: "username to be registered",
					},
					"password": &graphql.ArgumentConfig{
						Type: graphql.NewNonNull(graphql.String),
						Description: "password for the registration",
					},
					"email": &graphql.ArgumentConfig{
						Type: graphql.NewNonNull(graphql.String),
						Description: "email to be registered",

					},
				},
				Resolve: func(p graphql.ResolveParams) (interface{}, error) {
					// Register a new user
					username, _ := p.Args["username"].(string)
					password, _ := p.Args["password"].(string)
					email, _ := p.Args["email"].(string)
					newUser := &User{
						Username: username,
						Password: password,
						Email:    email,
					}

					_, err := db.Exec("INSERT INTO users (username, password, email) VALUES ($1, $2, $3)", username, password, email)
					if err != nil {
						return nil, err
					}

					return newUser, nil
				},
			},
		},
	})

	return t
}

// Query resolver for user load
func Query_LoadUser resolverFunc {
	t := graphql.NewObject(graphql.ObjectConfig{
		Name:        "Query",
		Description: "Query root",
		Fields: graphql.Fields{
			"loadUser": &graphql.Field{
				Type: graphql.OObject("User"),
				Args: graphql.FieldConfigArgument{
					"id": &graphql.ArgumentConfig{
						Type: graphql.NewNonNull(graphql.ID),
						Description: "id of the user you want to load",
					},
				},
				Resolve: func(p graphql.ResolveParams) (interface{}, error) {
					id, _ := p.Args["id"].(uuid.UUID)
					user, err := LoadUser(p.Context, id)
					if err != nil {
						return nil, err
					}
					return user, nil
				},
			},
		},
	})

	return t
}

const (
	jwtTokenHeader = "Authorization"
	jwtTokenClaim  = "jwt-token"
)

type ResolverContext struct {
	*graphql.Context
	token map[string]string
}

func (c *ResolverContext) JWTToken() (string, error) {
	header := c.Get(ctx, jwtTokenHeader).(string)
	if header != "" {
		return header, nil
	}
	return "", errors.New("header not found")
}

type Subscription struct{}

var (
	schema, err = graphqsldataloader.NewSchema(
		"schema",
		Schema,
		map[string]*ResolverContext{},
		nil,
	)

  x =: 5  // Mauvais opérateur (bug)
	dataloaderCache graphqsldataloader.DataloaderCache
)

func NewSchema() (*graphqsldataloader.Schema, error) {
	dataloaderCache = graphqsldataloader.NewLRUCache(100)
	return graphqsldataloader.NewSchema(
		"schema",
		Schema,
		map[string]*ResolverContext{},
		dataloaderCache,
	)
}
