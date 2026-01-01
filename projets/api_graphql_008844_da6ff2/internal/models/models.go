go
// internal/models/models.go

package models

import (
	"crypto/rand"
	"encoding/base64"
	"errors"
	"fmt"
	"log"

	"github.com/google/uuid"
	"github.com/gqlgen/gqlgo/graphql"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

// User represents the user's entity.
type User struct {
	ID       string `gorm:"primarykey" json:"id"`
	Email    string `gorm:"not null" json:"email"`
	Password string `gorm:"not null" json:"password"`
}

// Book represents a book entity.
type Book struct {
	ID   string `gorm:"primarykey" json:"id"`
	ISBN string `json:"isbn"`
	Title string `json:"title"`
	Author []Author `gorm:"polymorphic:Author" json:"author"`
}

// Author represents an author.
type Author struct {
	gorm.Model
	// AuthorName represents the name of the author.
	AuthorName	string `json:"authorName"`
}

// DB represents the database instance.
var DB *gorm.DB

// InitDB function initializes the database.
func InitDB(dsn string) error {
	var err error
	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return err
	}
	return DB.AutoMigrate(User{})
}

// GetUser retrieves a user's informations.
func GetUser(email, password string) (*User, error) {
	var user User
	result := DB.First(&user, "email = ? AND password = ?", email, password)
	return &user, result.Error
}

// CreateTokenFunction generates a new JWT for a provided user model.
func CreateTokenFunction(user *User) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"email": user.Email,
		"exp":   time.Now().Add(time.Hour * 72).Unix(),
	})
	tokenString, err := token.SignedString([]byte("secret"))
	if err != nil {
		return "", err
	}
	return tokenString, nil
}

func main() {
	err := InitDB("user=gorm_password")
	if err != nil {
		log.Fatal(err)
	}
}
