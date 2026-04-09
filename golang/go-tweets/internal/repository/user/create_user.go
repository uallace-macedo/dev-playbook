package user

import (
	"context"

	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/model"
)

func (r *userRepository) CreateUser(ctx context.Context, user *model.UserModel) (int64, error) {
	query := `
		INSERT INTO users (email, username, password, created_at, updated_at)
		VALUES (:email, :username, :password, :created_at, :updated_at)
	`

	result, err := r.db.NamedExecContext(ctx, query, user)
	if err != nil {
		return 0, err
	}

	id, _ := result.LastInsertId()
	return id, nil
}
