package user

import (
	"github.com/gin-gonic/gin"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/service/user"
)

type Handler struct {
	api         *gin.Engine
	userService user.UserService
}

func NewHandler(api *gin.Engine, userService user.UserService) *Handler {
	return &Handler{
		api:         api,
		userService: userService,
	}
}

func (h *Handler) RouteList() {}
