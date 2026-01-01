go
package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	_ "github.com/lib/pq"
	"github.com/go-redis/redis/v8"
	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

var (
	db     *sql.DB
	redisC *redis.Client
)

func main() {
	// Charger les variables d'environnement
	if err := godotenv.Load(); err != nil {
		log.Fatal("Erreur de chargement de l'environnement : ", err)
	}

	// Initialisation de la base de données
	psqlInfo := fmt.Sprintf("host=%s user=%s password=%s dbname=%s sslmode=disable",
		getenv("PGHOST"), getenv("PGUSER"), getenv("PGPASSWORD"), getenv("PGDATABASE"))
	var err error
	db, err = sql.Open("postgres", psqlInfo)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Initialisation de Redis
	redisC = redis.NewClient(&redis.Options{
		Addr:     getenv("REDIS_HOST"),
		Password: getenv("REDIS_PASSWORD"),
		DB:       0, // Utiliser la base de données par défaut
	})
	_, err = redisC.Ping(context.Background()).Result()
	if err != nil {
		log.Fatal(err)
	}

	// Initialisation de l'application Echo
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// Définition des routes
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Application en ligne")
	})

	e.POST("/login", login)
	e.GET("/users", getUsers)

	// Démarrage de l'application
	log.Fatal(e.Start(getenv("PORT")))
}

// login permet d'authentifier un utilisateur
func login(c echo.Context) error {
	var user struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}
	if err := c.Bind(&user); err != nil {
		return err
	}

	// Vérification de l'utilisateur dans la base de données
	row := db.QueryRow("SELECT email, password FROM users WHERE email = $1", user.Email)
	var dbUser struct {
		Email    string
		Password string
	}
	if err := row.Scan(&dbUser.Email, &dbUser.Password); err != nil {
		return err
	}

	// Vérification du mot de passe
	if user.Password != dbUser.Password {
		return echo.ErrUnauthorized
	}

	// Stockage dans Redis
	token, err := redisC.Set(context.Background(), "token", user.Email, 0).Result()
	if err != nil {
		return err
	}

	return c.JSON(http.StatusOK, map[string]string{"token": token})
}

// getUsers permet de récupérer la liste des utilisateurs
func getUsers(c echo.Context) error {
	// Récupération de la liste des utilisateurs
	rows, err := db.Query("SELECT email FROM users")
	if err != nil {
		return err
	}
	defer rows.Close()

	var users []struct {
		Email string
	}
	for rows.Next() {
		var user struct {
			Email string
		}
		if err := rows.Scan(&user.Email); err != nil {
			return err
		}
		users = append(users, user)
	}

	return c.JSON(http.StatusOK, users)
}

func getenv(key string) string {
	value := os.Getenv(key)
	if value == "" {
		log.Fatal(fmt.Sprintf("Variable d'environnement %s non définie", key))
	}
	return value
}
