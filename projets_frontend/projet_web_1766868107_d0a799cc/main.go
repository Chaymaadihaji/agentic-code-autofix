go
package main

import (
	"context"
	"crypto/rand"
	"crypto/rsa"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
	"github.com/lib/pq"
	"github.com/pkg/errors"
	"github.com/redis/go-redis/v9"
)

// User represent a user
type User struct {
	ID       uint   `json:"id"`
	Username string `json:"username"`
	Password string `json:"password"`
}

// Database represents a PostgreSQL database
type Database struct {
	*sql.DB
}

// NewDatabase returns a new Database instance
func NewDatabase(dsn string) (*Database, error) {
	db, err := sql.Open("postgres", dsn)
	if err != nil {
		return nil, errors.Wrap(err, "failed to open database")
	}

	if err := db.Ping(); err != nil {
		return nil, errors.Wrap(err, "ping database failed")
	}

	return &Database{DB: db}, nil
}

// Redis represents a Redis client
type Redis struct {
	*redis.Client
}

// NewRedis returns a new Redis instance
func NewRedis(addr string) (*Redis, error) {
	client := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	if _, err := client.Ping(context.Background()).Result(); err != nil {
		return nil, errors.Wrap(err, "ping Redis failed")
	}

	return &Redis{Client: client}, nil
}

// GenerateKey generates a random key
func GenerateKey() (string, error) {
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return "", errors.Wrap(err, "failed to generate key")
	}

	return fmt.Sprintf("%x", privateKey.PublicKey.N), nil
}

// UserHandler handles user-related requests
type UserHandler struct {
	db  *Database
	redis *Redis
}

// NewUserHandler returns a new UserHandler instance
func NewUserHandler(db *Database, redis *Redis) *UserHandler {
	return &UserHandler{db: db, redis: redis}
}

func (u *UserHandler) Register(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if _, err := u.db.Exec("INSERT INTO users (username, password) VALUES ($1, $2)", user.Username, user.Password); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	key, err := GenerateKey()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	u.redis.Set(context.Background(), fmt.Sprintf("user:%d", user.ID), key, 0)
	u.redis.Set(context.Background(), fmt.Sprintf("user:%s", user.Username), key, 0)

	w.WriteHeader(http.StatusCreated)
}

func (u *UserHandler) Login(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	var storedKey string
	if storedKey, err = u.redis.Get(context.Background(), fmt.Sprintf("user:%s", user.Username)).Result(); err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	if err := u.db.QueryRow("SELECT password FROM users WHERE username = $1", user.Username).Scan(&user.Password); err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	if user.Password != storedKey {
		http.Error(w, "invalid password", http.StatusUnauthorized)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func main() {
	dsn := "user:password@localhost/mydatabase"
	addr := "localhost:6379"

	db, err := NewDatabase(dsn)
	if err != nil {
		log.Fatal(err)
	}

	redis, err := NewRedis(addr)
	if err != nil {
		log.Fatal(err)
	}

	router := mux.NewRouter()

	userHandler := NewUserHandler(db, redis)

	router.HandleFunc("/register", userHandler.Register).Methods("POST")
	router.HandleFunc("/login", userHandler.Login).Methods("POST")

	log.Fatal(http.ListenAndServe(":8080", router))
}
