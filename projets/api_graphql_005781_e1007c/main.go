```go
// main.go

package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/graphql-go/handler"
	"github.com/graphql-go/plugin/auth/authz"
	"github.com/graphql-go/plugin/auth/jwt"
	v2 "github.com/graphql-go/plugin/resolver/v2"
	"github.com/graphql-go/plugin/subscription"
	"github.com/graphql-go/plugin/websocket"
	"github.com/graphql-go/plugin/wsconn"
	"github.com/graph-gophers/graphql-socket"
	"github.com/graph-gophers/graphql-go"
	"github.com/graph-gophers/graphql-go/errcode"
	"github.com/graph-gophers/graphql-go/keyword"
	"github.com/graph-gophers/graphql-go/subscription"
	"github.com/graph-gophers/graphql-go/utilities"
	"github.com/graphql-go/plugin/resolver/v2/example"
	"github.com/graphql-go/plugin/resolver/v2/user"
	"github.com/lib/pq"
	"github.com/okta/okta-sdk-go/okta"
	"github.com/okta/okta-sdk-go/services/users"
	"github.com/gorilla/websocket"
	"github.com/joho/godotenv"
	"github.com/graphql-go/subscription"
	"time"
)

func main() {
	// Chargement du fichier de configuration
	dotenv.Load(".env")

	// Initialisation de la base de données PostgreSQL
	dataSource := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
		os.Getenv("DB_HOST"), os.Getenv("DB_USER"), os.Getenv("DB_PASSWORD"), os.Getenv("DB_NAME"), os.Getenv("DB_PORT"))

	db, err := sql.Open("postgres", dataSource)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Initialisation de l'API GraphQL
	config := handler.Config{
		Schema:          &graphql.Schema{Query: Query},
		GenFiles:         true,
		Playground:       true,
		GraphiQLID:       "graphql",
		GraphID:          "graphql",
		AutoRegisterResolvers: true,
		ValidateResolvers: true,
	}
	h := handler.New(&config)

	// Initialisation de l'authentification en JWT
	jwtMiddleware, _ := jwt.New(jwt.WithSecret(os.Getenv("JWT_SECRET")), jwt.WithExpiration(int(uint64(os.Getenv("JWT_EXPIRATION")))))

	// Initialisation de la stratégie d'autorisation
	authStragegy := authz.New(jwtMiddleware)

	// Initialisation du plugin de résolution
	resolver := &resolver.Resolver{DB: db}

	// Définition de l'application
	app := http.NewServeMux()
	app.Use(authStragegy)
	app.Handle("/graphql", graphql.PlaygroundHandler("/graphql"))
	app.HandleFunc("/graphql", func(w http.ResponseWriter, r *http.Request) {
		c := context.Background()
		jwtClaims, err := jwtMiddleware.ParseFromAuthorizationHeader(os.Getenv("Authorization"))
		w.Header().Set("Content-Type", "application/json")
		if err == nil {
			resolver.JWT = jwtClaims
			log.Println(jwtClaims)
			json.NewEncoder(w).Encode(graphql.Do(c, &graphql.Context{Request: r, Writer: w, RespWriter: w}, authz.New(jwtMiddleware), resolver))
		} else {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
	})

	// Initialisation du plugin de socket
	graphqlSocket := graphql.GraphQLSocket(graphql.PlaygroundHandler("/graphql/socket"))

	// Initialisation du serveur WebSocket
	wsServer := func(ctx context.Context, c *websocket.Conn) {
		defer c.Close(1000, "")

		// Envoi de l'authentification WebSocket
		err := sendAuth(ctx, c, resolver)
		if err != nil {
			log.Println(err)
			c.Close(1000, "")
			return
		}

		// Réception et traitement des messages du client
		for {
			var message websocket.Message
			select {
			case <-ctx.Done():
				return
			case err := c.NextMessage(&message):
				if err != nil {
					log.Println(err)
					c.Close(1000, "")
					return
				}

				// Traitement des messages du client
				err = resolver.SocketMessage(c.Writer, message.Data, &graphql.Context{Request: c.Request()})
				if err != nil {
					log.Println(err)
					c.Close(1000, "")
					return
				}
			}
		}
	}

	uuid := "your-uuid"
	s := grpc.NewServer(grpc.WithStatsHandler(stats.New()))
	pb.RegisterWebSocketServiceServer(s, &grpc.WebSocketServer{UUID: uuid})
	http.Handle("/websocket", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_ = websocket.Upgrade(w, r, nil, 0, 0)
		serveWs(h, c)
	}))

	// Lancement du server HTTP
	log.Fatal(http.ListenAndServe(":8080", app))
}

func sendAuth(ctx context.Context, conn *websocket.Conn, resolver *resolver.Resolver) error {
	type auth struct {
		Token string `json:"token"`
	}

	var auth auth
	select {
	case <-ctx.Done():
		return nil
	default:
		_, _, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return err
		}
		json.NewDecoder(conn).Decode(&auth)
		resolver.JWT = jwt.NewToken(auth.Token)
		return resolver.auth(ctx, conn.WriteMessage(websocket.TextMessage, []byte("Auth OK")))
	}
}

func serveWs(h *handler, c ...interface{}) {
	wsServer := &WebSocketServer{
		Conn:  nil,
		Write: func(message interface{}) {
			log.Println(message)
		},
		h: h,
		c: c,
	}
	uuid := "your-uuid"
	go func() {
		for {
			wsServer.conn, wSerr := websocketUpgrader.Upgrade(wsServer.conn, r, nil, 0, 0)
			if wSerr != nil {
				log.Println("Failed to set up WebSocket connection:", wSerr)
				continue
			}
			uuid := "your-uuid"
			resolver := *WebSocketServer.UUID
			h := &handler{Conn: wsServer.conn, Write: func(message interface{}) {
				log.Println(message)
			}}
			c := context.Background()

			go func() {
				for {
					select {
					case <-c.Done():
						wsServer.conn.Close(1000, ""))
					default:
						type auth struct {
							Token string `json:"token"`
						}
						var auth auth
						if connErr := wsServer.conn.ReadJSON(&auth); connErr != nil {
							break
						}
						resolver.JWT = jwt.NewToken(auth.Token)
						log.Println(auth.Token)
					}
				}
			}()

			select {
			case <-c.Done():
				wsServer.conn.Close(1000, "")
				continue
			default:
				h.Conn.WriteMessage(websocket.TextMessage, []byte("connected"))
				h.Conn.WriteMessage(websocket.TextMessage, []byte(`{
					"result": "connected"
				}`))
				for {
					wsServer.conn.WriteMessage(websocket.TextMessage, []byte(`{
						"result": "message received"
					}`))
				}
			}
		}
	}()
}

type Resolver struct {
	DB          *sql.DB
	JWT         *jwt.Claim
}

type WebSocketServer struct {
	UUID string
	Conn *websocket.Conn
}

type SocketMessage struct {
	Type      string
	Data      []byte
	Conn      *websocket.Conn
	Context   *graphql.Context
}

func (r *Resolver) auth(ctx context.Context, m interface{}) error {
	return nil
}

func (r *Resolver) SocketMessage(w *websocket.Writer, message []byte, c *graphql.Context) error {
	log.Println(r.JWT)
	return nil
}

func Query() *graphql.Schema {
	return &graphql.Schema{
		Mutation: &graphql.Object{
			Name:   "Mutation",
			Fields: graphql.Fields{
				"login": &graphql.Field{
					Type:        "String",
					Args:        graphql.FieldConfigArgument{},
					Description: "login",
					Resolver: func(p graphql.ResolveParams) (interface{}, error) {
						user := user.Login(p.Args["username"].(string), p.Args["password"].(string))
						return user, nil
					}},
				},
				"signup": &graphql.Field{
					Type:        "String",
					Args:        graphql.FieldConfigArgument{},
					Description: "Register a user and login",
					Resolver: func(p graphql.ResolveParams) (interface{}, error) {
						user := user.Signup(p.Args["username"].(string), p.Args["email"].(string), p.Args["password"].(string), os.Getenv("COOKIE_TOKEN"))
						return user, nil
					}},
			},
		},
		Query: &graphql.Object{
			Name:   "Query",
			Fields: graphql.Fields{
				"user": &graphql.Field{
					Type:        keyword.String,
					Args:        graphql.FieldConfigArgument{},
					Description: "Get user info",
					Resolver: func(p graphql.ResolveParams) (interface{}, error) {
						user
