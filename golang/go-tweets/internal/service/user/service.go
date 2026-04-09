package user

import (
	"context"

	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/config"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/dto"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/repository/user"
)

type UserService interface {
	Register(ctx context.Context, req *dto.RegisterRequest) (int64, int, error)
}

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
