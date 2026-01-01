go
// Package models contient les définitions des modèles de données de l'application.
package models

import (
	"context"
	"database/sql"
	"time"

	"github.com/go-redis/redis/v9"
	"github.com/lib/pq"
)

// User représente un utilisateur de l'application.
type User struct {
	ID       int       `json:"id"`
	Username string    `json:"username"`
	Email    string    `json:"email"`
	Password string    `json:"-"`
	Created  time.Time `json:"created"`
	Updated  time.Time `json:"updated"`
}

// UserCache est un modèle pour stocker les données d'un utilisateur dans Redis.
type UserCache struct {
	ID       string `json:"id"`
	Username string `json:"username"`
	Email    string `json:"email"`
	Expires  time.Time
}

// Database est une interface pour interagir avec la base de données PostgreSQL.
type Database interface {
	Conn() (*sql.DB, error)
}

// RedisClient est une interface pour interagir avec le client Redis.
type RedisClient interface {
	Get(ctx context.Context, key string) (*redis.StringCmd, error)
	Set(ctx context.Context, key string, value string, expiration time.Duration) (*redis.StatusCmd, error)
}

// UserRepository est une interface pour gérer les opérations sur les utilisateurs.
type UserRepository interface {
	GetUser(ctx context.Context, id int) (*User, error)
	GetUserByUsername(ctx context.Context, username string) (*User, error)
	CreateUser(ctx context.Context, user *User) error
}

// CacheRepository est une interface pour gérer les opérations sur le cache.
type CacheRepository interface {
	GetUserCache(ctx context.Context, id int) (*UserCache, error)
	SetUserCache(ctx context.Context, id int, cache *UserCache) error
}

// userRepositoryImpl est une implémentation de UserRepository.
type userRepositoryImpl struct {
	db Database
}

// NewUserRepository retourne une nouvelle instance de UserRepository.
func NewUserRepository(db Database) UserRepository {
	return &userRepositoryImpl{db: db}
}

// GetUser retourne l'utilisateur correspondant à l'ID donné.
func (r *userRepositoryImpl) GetUser(ctx context.Context, id int) (*User, error) {
	user := &User{}
	err := r.db.Conn().QueryRowContext(ctx, "SELECT * FROM users WHERE id = $1", id).Scan(user)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, sql.ErrNoRows
		}
		return nil, err
	}
	return user, nil
}

// GetUserByUsername retourne l'utilisateur correspondant au nom d'utilisateur donné.
func (r *userRepositoryImpl) GetUserByUsername(ctx context.Context, username string) (*User, error) {
	user := &User{}
	err := r.db.Conn().QueryRowContext(ctx, "SELECT * FROM users WHERE username = $1", username).Scan(user)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, sql.ErrNoRows
		}
		return nil, err
	}
	return user, nil
}

// CreateUser crée un nouvel utilisateur.
func (r *userRepositoryImpl) CreateUser(ctx context.Context, user *User) error {
	_, err := r.db.Conn().ExecContext(ctx, "INSERT INTO users (username, email, password) VALUES ($1, $2, $3)", user.Username, user.Email, user.Password)
	return err
}

// cacheRepositoryImpl est une implémentation de CacheRepository.
type cacheRepositoryImpl struct {
	r RedisClient
}

// NewCacheRepository retourne une nouvelle instance de CacheRepository.
func NewCacheRepository(r RedisClient) CacheRepository {
	return &cacheRepositoryImpl{r: r}
}

// GetUserCache retourne le cache utilisateur correspondant à l'ID donné.
func (r *cacheRepositoryImpl) GetUserCache(ctx context.Context, id int) (*UserCache, error) {
	cache := &UserCache{}
	key := fmt.Sprintf("user:%d", id)
	cmd := r.r.Get(ctx, key)
	err := cmd.Err()
	if err != nil {
		return nil, err
	}
	err = cmd.Scan(cache)
	if err != nil {
		return nil, err
	}
	return cache, nil
}

// SetUserCache stocke le cache utilisateur pour l'ID donné.
func (r *cacheRepositoryImpl) SetUserCache(ctx context.Context, id int, cache *UserCache) error {
	key := fmt.Sprintf("user:%d", id)
	return r.r.Set(ctx, key, cache.Username, cache.Expires.Sub(time.Now())).Err()
}
