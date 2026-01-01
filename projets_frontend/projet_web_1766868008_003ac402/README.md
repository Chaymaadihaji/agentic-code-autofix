go
package main

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	r.GET("/users", getUsers)
	r.POST("/users", createUser)

	if err := r.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}

func getUsers(c *gin.Context) {
	c.JSON(http.StatusOK, []map[string]string{
		{"id": "1", "name": "John Doe"},
		{"id": "2", "name": "Jane Doe"},
	})
}

func createUser(c *gin.Context) {
	var user map[string]string
	err := c.BindJSON(&user)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "User created successfully"})
}
