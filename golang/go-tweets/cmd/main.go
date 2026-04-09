package main

import (
	"github.com/gin-gonic/gin"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/config"

	userHandler "github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/handler/user"
	userRepo "github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/repository/user"
	userService "github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/service/user"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/pkg/internalsql"
)

func main() {
	l := config.NewLogger("")
	cfg, err := config.LoadConfig(l)

	if err != nil {
		l.Error(err)
		return
	}

	db, err := internalsql.ConnectMySQL(cfg)
	if err != nil {
		l.Error(err)
		return
	}

	l.Info("db connected")

	r := gin.Default()
	r.Use(gin.Recovery())

	userRepo := userRepo.NewUserRepository(db)
	userService := userService.NewUserService(cfg, userRepo)
	userHandler := userHandler.NewHandler(r, userService)
	userHandler.RouteList()

	r.Run(cfg.APIPort)
}
