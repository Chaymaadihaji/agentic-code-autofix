go
// handlers/handlers.go
package handlers

import (
	"context"
	"log"
	"net/http"
	"strconv"

	"github.com/graphql-golang/graphql/handler"
	"github.com/graphql-golang/graphql/handler/transport"
	wsTransport "github.com/graphql-golang/graphql/transport/websocket"
	"github.com/gorilla/websocket"
	gqlgen "github.com/vektah/gql-gen/graphql/handler"
	"github.com/vektah/gql-gen/graphql/executor"
	"github.com/vektah/gql-gen/graphql/operation"
	h "k8s.io/kubectl/pkg/cmd/config/current-context"
	v1 "k8s.io/kubelets/apis/settings/api/v1"
	k8serrors "k8s.io/kubernetes/pkg/api/v1"
	"k8s.io/kubernetes/pkg/kubelet/volume/volumetypes"

	postgresDB "github.com/lib/pq"

	"github.com/graphql-golang/graphql-go"
	"github.com/graphql-golang/graphql-go/handler/graphqlplayground"
	"github.com/graphql-golang/graphql-go/handler/transport/websocketplayground"
	jwt "github.com/dgrijalva/jwt-go"
)

const (
	SECRET_KEY = "supersecret"
	TABLE_NAME = "users"
)

// Conn is used to get connection pool
type Conn struct {
	*postgresDB.Conn
}

// NewHandler return a new instance of GraphQL Handler
func (conn Conn) NewHandler(ctx context.Context, jwt *jwt.Token, username string) *gqlgen.Handler {
	resolver := &GqlGen Resolver{Conn: conn}
	token := jwt.Claims
	return gqlgen.NewHandler(graphql.NewSchema(
		&graphql.Schema{Query: graphql.NewObject(
		 graphql.ObjectConfig{
			 Name: "Query",
			 Fields: graphql.FieldConfigDefinition{
				 &graphql.Field{
					 Name:        "user",
					 Description: "Get user",
					 Type: graphql.String,
					 Args: graphql.FieldConfigArgument{
						"name": &graphql.ArgumentConfig{
							Name: "name",
							Type: graphql.String,
						},
					},
				 Resolvers: map[string]graphql.Resolver{
					 "user": resolver.GetUser,
				 },
					 ArgsFunc: func() map[string]interface{} {return map[string]interface{}{"username": username }},
				 },
				 &graphql.Field{
					 Name: "subscriptions",
					 Description: "Subscribe to messages",
					 Type:       graphql.GraphQLSubscription,
					 Args:       graphql.FieldConfigArgument{},
					 ArgsFunc: func() map[string]interface{} {return map[string]interface{}{"username": username }},
					 Resolve: func(p graphql.ResolveParams) (interface{}, error) {
						 return nil, nil  //TODO: implement subscription
					 },
					 },
				 },
		 },
		)},
	), jwt,
	ctx,
	conn.Conn,
	websocketplayground.New(playground.HandlerOptions{
		RootHTML: template.ExecuteString(ctx, "index"),
	}), webTransport(),
	graphqlplayground.GetHandler(),
	)
}

// NewHandler return a new instance of GraphQL Handler
func NewHandler(ctx context.Context) *gqlgen.Handler {
	jwtToken, err := jwt.Parse(secretKey)
	if err != nil {
		log.Println(err)
		return nil
	}
	resolver := &GqlGen Resolver{}
	token := jwtToken.Claims
	return gqlgen.NewHandler(graphql.NewSchema(
		&graphql.Schema{Query: graphql.NewObject(
		 graphql.ObjectConfig{
			 Name: "Query",
			 Fields: graphql.FieldConfigDefinition{
				 &graphql.Field{
					 Name:        "user",
					 Description: "Get user",
					 Type: graphql.String,
					 Args: graphql.FieldConfigArgument{
						"name": &graphql.ArgumentConfig{
							Name: "name",
							Type: graphql.String,
						},
					},
				 Resolvers: map[string]graphql.Resolver{
					 "user": resolver.GetUser,
				 },
				 },
				 &graphql.Field{
					 Name: "subscriptions",
					 Description: "Subscribe to messages",
					 Type:       graphql.GraphQLSubscription,
					 Args:       graphql.FieldConfigArgument{},
					 Resolve: func(p graphql.ResolveParams) (interface{}, error) {
						 return nil, nil  //TODO: implement subscription
					 },
					 },
				 },
		 },
		)},
	), nil,
	ctx,
	nil,
	transport.DefaultHTTPHeaders,
	),
	)
}

func webTransport() transport.Transport {
	log.Println("Setting up WebSocket transport")
	upgrader := new(websocket.Upgrader)
	upgrader.CheckOrigin = func(r *http.Request) bool {
		secChans := r.TLS == nil ? 0 : len(r.TLS.ServerName)
		isLocalhost := r.Header.Get("Origin") == "null" || r.Header.Get("Origin") == "http://" || r.Header.Get("Origin") == "https://"
		return r.Remote Addr
	  //return r.IsLocal()
	}
	return &wsTransport.Websocket{
		Upgrader: websocket.Upgrader{
			ReadBufferSize:    4096,
			WriteBufferSize:   4096,
			Subprotocols:      nil,
			Subprotocol:       "",
			BufferPool:        new(BufferPool),
			ReadBufferSize:     0,
			WriteBufferSize:    0,
			OriginChecker: upgrader.CheckOrigin, // default is the default one
			CheckOrigin: func(r *http.Request) bool { //
				return true;
			},
		},
		Writer:       &wsTransport.Writer{} ,
		Reader:       &wsTransport.Reader{},
		OnConnect: func() (interface{}, error) {
			return nil, nil
		},
	}
}

// secretKey
const secretKey = "supersecret"

// AuthMiddleware check if user is authenticated
func AuthMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		authToken, err := r.Context().Value("auth").(*jwt.Token)
		if err != nil {
			http.Error(w, "You are not authenticated.", http.StatusForbidden)
            return
		}
		token := jwt.NewWithClaims()
		token.Claims = jwt.MapClaims{
			"username": strconv.Itoa(int(usernameID)), "iat": int64(0)}

		ctx:=context.WithValue(r.Context(), "auth", token)

		r = r.WithContext(ctx)
        next(w, r)
       }
}

// Middleware return a middleware function to inject authentication
func Middleware(next http.HandlerFunc) (result http.HandlerFunc) {
  token, err := jwt.Parse(secretKey) // token contains authentication information
  if err != nil {
        http.Error(w,  "Failed to get secret key", http.StatusInternalServerError)
        return
  }

  return func(w http.ResponseWriter, r *http.Request) {
          if token.Valid {
                  tokenValue := r.URL.Query().Get("token")  // retrieve auth token from query param
                  auth, err := jwt.ParseWithClaims(tokenValue, map[string]interface{}{},"")  // parse auth token using secret key

                  if err == nil && auth.Valid {
                context := context.WithValue(r.Context(), "auth", auth)  // inject auth token into request context
                r = r.WithContext(context)
                next(w,r)  // proceed to actual request handler

                return 
            }
            http.Error(w, "Authentication failed", http.StatusUnauthorized)
            return
	 }
 }
