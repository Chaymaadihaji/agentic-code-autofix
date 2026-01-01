go
// main.go

package main

import (
	"context"
	"database/sql"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/graph-gophers/gql-go/gqlparser/ast"
	"github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/gqlerrors"
	"github.com/graphql-go/graphql-go/gc"
	"github.com/graphql-go/subscriptions"
	"github.com/gorilla/websocket"
	"github.com/graphql-go/gqlschema"
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
	"github.com/lib/pq"
)

var db *sql.DB

func main() {
	loadEnv()

	// Connexion à la base de données
	var err error
	db, err = sql.Open("postgres", os.Getenv("DATABASE_URL"))
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Chargement du schéma de GraphQL
	schema, err := gqlschema.LoadSchema("schema.graphqls")
	if err != nil {
		log.Fatal(err)
	}

	// Création du générateur de GraphQL
	gc := gql.NewSchema(schema)

	// Création des routes GraphQL
	router := http.NewServeMux()
	router.HandleFunc("/api/graphql", func(w http.ResponseWriter, r *http.Request) {
		graphql.ServeHTTP(w, r, gc)
	})

	// Authentification JWT
	jwtToken := gin.jwt.New(
		gin.jwt.WithSigningMethod(gin.jwt.RSASigningMethodHmacSHA256WithSHA256),
		gin.jwt.WithKey(os.Getenv("JWT_SECRET")),
	)
	authorizer := gin.AuthAuthorizer()

	router.HandleFunc("/api/token", func(w http.ResponseWriter, r *http.Request) {
		tokenString := jwtToken.New()
		token := gin.jwt.NewToken(tokenString)
		// Gérer la création du token
		w.WriteHeader(http.StatusOK)
		w.Write(tokenString.Bytes())
	})

	// Gestion des connexions WebSocket
	upgrader := websocket.Upgrader{
		CheckOrigin: func(r *http.Request) bool {
			return true
		},
		HandshakeTimeout: 5 * time.Second,
	}
	subsConn := wsConn.NewSubscriptionConn()

	wsRouter := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Println(err)
			return
		}
		subs := &WebSocketSubscription{
			conn:               conn,
			subsManager:        subsConn,
			wsUpgrader:         upgrader,
			subscriptionManager: gc.GetSubscriptionHandler(),
		}
		subscribeHandler(subs.Conn)
	})

	// Gestion des requêtes GraphQL sous forme de subscription
	router.HandleFunc("/api/subscriptions", func(w http.ResponseWriter, r *http.Request) {
		wsRouter(w, r)
	})

	// Afficher les routes
	router.HandleFunc("/api/docs", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodGet {
			schema.GetQuery(w)
		} else {
			w.WriteHeader(http.StatusMethodNotAllowed)
		}
	})

	// Exécution de l'application GraphQL
	authorizer.AuthorizeRequest = gin.funcAuthAuthorizerFunc(func(req *gin.Request) bool {
		token, err := jwtToken.ParseHeaderAuthorization(req.GetHeader("token"))
		if err != nil {
			return false
		}
		return token.Valid()
	})

	gin.SetRouter(router)
	gin.SetMode(gin.ReleaseMode)
	gin.Run(":4000")
}

// WebSocketSubscription
type WebSocketSubscription struct {
	conn               *websocket.Conn
	subsManager        *wsConn
	wsUpgrader         Upgrader
	subscriptionManager SubscriptionHandler
}

// Subscribe
func (ws *WebSocketSubscription) Subscribe(req *graphQL.Request) *graphQL.Subscription {
	sub, err := ws.subscriptionManager.Subscribe(req)
	if err != nil {
		log.Println(err)
		return nil
	}

	ws.subsManager.Add(sub)
	sub.OnComplete(func(ctx context.Context) {
		ws.subsManager.Remove(sub)
	})

	sub.OnData(func(ctx context.Context, event *ast.Event) {
		if event.Operation.Kind == ast.OperationKind.Query || event.Operation.Kind == ast.OperationKind.Mutation {
			graphql.HandleEvent(ctx, event)
		}

		ws.conn.WriteMessage(websocket.TextMessage, event.String())
	})
	return sub
}

func loadEnv() {
	if err := godotenv.Load(); err != nil {
		log.Fatal(err)
	}
	if os.Getenv("DATABASE_URL") == "" {
		log.Fatal("DATABASE_URL est vide")
	}
}

type Upgrader struct{}

func (u *Upgrader) Upgrade(c *http.Client, req *http.Request) (*websocket.Conn, error) {
	return nil, nil
}

type SubscriptionHandler interface {
	Subscribe(req *graphql.Request) (*graphql.Subscription, error)
}

func subscribeHandler(conn *websocket.Conn) {
	// Gérer la connexion websocket
}

type wsConn struct{}

func NewSubscriptionConn() *wsConn {
	return &wsConn{}
}

func (ws *wsConn) Add(sub *websocket.Conn) {
	// Gérer l'ajout de la connexion websocket
}

func (ws *wsConn) Remove(sub *websocket.Conn) {
	// Gérer la suppression de la connexion websocket
}
