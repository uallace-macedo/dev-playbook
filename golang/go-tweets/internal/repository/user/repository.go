package user

import (
	"context"

	"github.com/jmoiron/sqlx"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/model"
)

type UserRepository interface {
	GetUserByEmailOrUsername(ctx context.Context, email, username string) (*model.UserModel, error)
	CreateUser(ctx context.Context, user *model.UserModel) (int64, error)
}

type userRepository struct {
	db *sqlx.DB
}

func NewUserRepository(db *sqlx.DB) *userRepository {
	return &userRepository{db: db}
}
