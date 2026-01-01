go
// Package handlers définit les handlers de l'API GraphQL
package handlers

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/google/uuid"
	"github.com/gophish/gophish/db"
	"github.com/gophish/gophish/models"
	"github.com/gophish/gophish/schema"
	"github.com/graphql-go/graphql/gqlerrors"
	"github.com/jmoiron/sqlx"
	"github.com/labstack/echo/v4"
	"github.com/joho/godotenv"
	"github.com/nfnt/resize"
	"github.com/pkg/errors"
	"github.com/tencentyun/cos-go-sdk-v5"
	"github.com/tencentyun/cos-go-sdk-v5/cos"
)

// ctxKeyDef permet d'identifier la clé de context dans les requêtes
const ctxKeyDef = "definition"

// Handler struct
type Handler struct {
	definition       string
	db               *sqlx.DB
	uploads          bool
	baseurl          string
	privateKey       string
	privateKeyID     string
	region           string
}

// NewHandler crée un nouveau Handler
func NewHandler(d *schema.Definition, u bool, db *sqlx.DB, b, p, pi, r string) *Handler {
	return &Handler{
		definition:       d.Description,
		db:               db,
		uploads:          u,
		baseurl:          b,
		privateKey:       p,
		privateKeyID:     pi,
		region:           r,
	}
}

// ServeHTTP gère les requêtes HTTP de l'API
func (h *Handler) ServeHTTP(c echo.Context) error {
definition := c.Get(ctxKeyDef).(schema.Definition)

	switch c.Request.Method {
	case http.MethodOptions:
		return h.handleOptions(c, definition)
	case http.MethodGet:
		return h.handleGet(c, definition)
	case http.MethodPost:
		return h.handlePost(c, definition)
	case http.MethodPut:
		return h.handlePut(c, definition)
	case http.MethodDelete:
		return h.handleDelete(c, definition)
	default:
		return echo.NewHTTPError(http.StatusMethodNotAllowed)
	}
}

func (*Handler) handleOptions(c echo.Context, d schema.Definition) error {
	return c.NoContent(http.StatusOK)
}

// handleGet gère les requêtes GET
func (h *Handler) handleGet(c echo.Context, d schema.Definition) error {
	switch d.GetQuery {
	case "user":
		return h.getUser(c, d.UserID)
	default:
		return echo.NewHTTPError(http.StatusNotFound, "ressource introuvable")
	}
}

func (h *Handler) getUser(c echo.Context, id string) error {
	user := models.User{}
	if err := h.db.Get(&user, "SELECT * FROM users WHERE id = $1", id); err != nil {
		return db.NewError(err)
	}
	if err := c.Set(ctxKeyDef, d); err != nil {
		return err
	}
	return c.JSON(http.StatusOK, user)
}

// handlePost gère les requêtes POST
func (h *Handler) handlePost(c echo.Context, d schema.Definition) error {
	switch d.PostQuery {
	case "createUser":
		return h.createUser(c)
	default:
		return echo.NewHTTPError(http.StatusNotFound, "ressource introuvable")
	}
}

func (h *Handler) createUser(c echo.Context) error {
	var user models.User
	if err := json.NewDecoder(c.Request().Body).Decode(&user); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest)
	}
	return h.db.MustExec(`INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *`, user.Name, user.Email).Scan(&user)
}

// handlePut gère les requêtes PUT
func (h *Handler) handlePut(c echo.Context, d schema.Definition) error {
	switch d.PutQuery {
	case "updateUser":
		return h.updateUser(c)
	default:
		return echo.NewHTTPError(http.StatusNotFound, "ressource introuvable")
	}
}

func (h *Handler) updateUser(c echo.Context) error {
	var user models.User
	if err := json.NewDecoder(c.Request().Body).Decode(&user); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest)
	}
	if err := h.db.Query(`UPDATE users SET name = $1, email = $2 WHERE id = $3 RETURNING *`, user.Name, user.Email, user.ID).Scan(&user); err != nil {
		return db.NewError(err)
	}
	return c.JSON(http.StatusOK, user)
}

// handleDelete gère les requêtes DELETE
func (h *Handler) handleDelete(c echo.Context, d schema.Definition) error {
	switch d.DeleteQuery {
	case "deleteUser":
		return h.deleteUser(c)
	default:
		return echo.NewHTTPError(http.StatusNotFound, "ressource introuvable")
	}
}

func (h *Handler) deleteUser(c echo.Context) error {
	if err := h.db.Exec(`DELETE FROM users WHERE id = $1`, "some-user-id").RowsAffected; err != nil {
		return db.NewError(err)
	}
	if err := sqlx.PgQueryContext(h.db,
		`CREATE TABLE users_old (
			name text,
			email text
		)`
	).Close() == nil; err != nil {
	return db.NewError(err)
	}
	if err := sqlx.PgQueryContext(h.db,
		`INSERT INTO users_old (name, email) SELECT name, email FROM users`
	).Close() == nil; err != nil {
	return db.NewError(err)
	}
	return c.NoContent(http.StatusOK)
}

func (*Handler) main() {
	handlers := handlers.NewHandler(schema.Definition{
		Name:  "api",
		Query: "user",
	}, true, db.GetConnectionDB(), "baseurl.com",
		privateKey, privateKeyID, region)
    if err := godotenv.Load(); err != nil {
		log.Fatal(err)
	}
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	handlers.Register(e.Group("/GraphQL"))
	e.HideLogo = true
	e.Logger.Fatal(e.Start(":1323"))
}
