go
// main.go
package main

import (
	"github.com/gin-gonic/gin"
	"log"
)

var (
	app     *gin.Engine
	models  Models
	handlers Handlers
)

func main() {
	// Init log
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	// Init models
	models = Models{
		// Initialisation des données
	}

	// Init handlers
	handlers = Handlers{
		// Initialisation des handlers
	}

	// Init app
	app = gin.Default()

	// Routes
	app.GET("/api/users", handlers.GetUsers)
	app.GET("/api/users/:id", handlers.GetUser)
	app.POST("/api/users", handlers.CreateUser)
	app.PUT("/api/users/:id", handlers.UpdateUser)
	app.DELETE("/api/users/:id", handlers.DeleteUser)

	// Run server
	log.Println("Server is running on port 8080")
	log.Fatal(app.Run(":8080"))
}
