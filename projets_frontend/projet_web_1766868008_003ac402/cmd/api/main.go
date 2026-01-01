go
// cmd/api/main.go

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/swaggo/gin-swagger"
	"github.com/swaggo/gin-swagger/swaggerFiles"
)

type Server struct {
	router *gin.Engine
}

func NewServer() *Server {
	return &Server{
		router: gin.New(),
	}
}

func (s *Server) Run(addr string) {
	s.router.GET("/swagger/*any", swaggerFiles.SwaggerUI)

	v1 := s.router.Group("/api/v1")

	v1.GET("/users", getUsers)
	v1.GET("/users/:id", getUser)

	v1.POST("/users", createUser)
	v1.PUT("/users/:id", updateUser)
	v1.DELETE("/users/:id", deleteUser)

	s.router.Run(addr)
}

func main() {
	if v := os.Getenv("GIN_MODE"); v != "release" {
		gin.SetMode(gin.DebugMode)
	}

	srv := NewServer()

 addr := fmt.Sprintf(":%s", os.Getenv("PORT"))
 srv.Run(addr)

 log.Println("Server listening on", addr)

 signalChan := make(chan os.Signal, 1)
 signal.Notify(signalChan, os.Interrupt)

 <-signalChan
 log.Println("Server shutting down...")

 ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
 defer cancel()

 if err := srv.router.Unscoped().Shutdown(ctx); err != nil {
  log.Fatal(err)
 }

 log.Println("Server shutdown complete")
}
