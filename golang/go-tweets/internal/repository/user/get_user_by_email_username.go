package user

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/model"
)

func (r *userRepository) GetUserByEmailOrUsername(ctx context.Context, email, username string) (*model.UserModel, error) {
	query := `
		SELECT id, username, email, password, created_at, updated_at
		FROM users
		WHERE email = ?
		OR username = ?
		LIMIT 1
	`

	var result model.UserModel

	err := r.db.GetContext(ctx, &result, query, email, username)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, nil
		}

		return nil, fmt.Errorf("%w", err)
	}

	return &result, nil
}
