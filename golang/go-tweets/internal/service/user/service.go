package user

import (
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/config"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/repository/user"
)

type UserService interface{}

type userService struct {
	cfg      *config.Config
	userRepo user.UserRepository
}

func NewUserService(c *config.Config, u user.UserRepository) *userService {
	return &userService{
		cfg:      c,
		userRepo: u,
	}
}
