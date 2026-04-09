package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/config"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/pkg/internalsql"
)

func main() {
	l := config.NewLogger("")
	cfg, err := config.LoadConfig(l)

	if err != nil {
		l.Error(err)
		return
	}

	_, err = internalsql.ConnectMySQL(cfg)
	if err != nil {
		l.Error(err)
		return
	}

	l.Info("db connected")

	r := gin.Default()
	r.Use(gin.Recovery())

	r.GET("/check-health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "OK",
		})
	})

	r.Run(cfg.APIPort)
}
