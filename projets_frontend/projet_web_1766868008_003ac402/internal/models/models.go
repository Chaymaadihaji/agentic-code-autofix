go
// Package models définit les modèles pour l'application API.
package models

import (
	"gorm.io/gorm"
)

// User représente un utilisateur dans l'application.
type User struct {
	gorm.Model
	Name     string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

// Book représente un livre dans l'application.
type Book struct {
	gorm.Model
	Title       string `json:"title"`
	Author      string `json:"author"`
	Description string `json:"description"`
}

// NewUser crée un nouvel utilisateur avec les informations fournies.
func NewUser(name, email, password string) (*User, error) {
	user := User{
		Name:     name,
		Email:    email,
		Password: password,
	}
	err := user.Validate()
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// Validate vérifie que les informations de l'utilisateur sont valides.
func (u *User) Validate() error {
	if u.Name == "" || u.Email == "" || u.Password == "" {
		return ErrorInvalidInput
	}
	return nil
}

// ErrorInvalidInput est une erreur personnalisée pour les entrées invalides.
var ErrorInvalidInput = "invalid input"

// NewBook crée un nouveau livre avec les informations fournies.
func NewBook(title, author, description string) (*Book, error) {
	book := Book{
		Title:       title,
		Author:      author,
		Description: description,
	}
	err := book.Validate()
	if err != nil {
		return nil, err
	}
	return &book, nil
}

// Validate vérifie que les informations du livre sont valides.
func (b *Book) Validate() error {
	if b.Title == "" || b.Author == "" || b.Description == "" {
		return ErrorInvalidInput
	}
	return nil
}
