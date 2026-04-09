package user

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/dto"
	"github.com/uallace-macedo/dev-playbook/golang/go-tweets/internal/model"
	"golang.org/x/crypto/bcrypt"
)

func (s *userService) Register(ctx context.Context, req *dto.RegisterRequest) (int64, int, error) {
	// check user already exists
	userExist, err := s.userRepo.GetUserByEmailOrUsername(ctx, req.Email, req.Username)

	if err != nil {
		return 0, http.StatusInternalServerError, err
	}

	if userExist != nil {
		return 0, http.StatusBadRequest, fmt.Errorf("user already exists")
	}

	// hash password

	if req.Password != req.PasswordConfig {
		return 0, http.StatusBadRequest, fmt.Errorf("passwords dont match")
	}

	passwordHash, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return 0, http.StatusInternalServerError, err
	}

	now := time.Now()
	userModel := &model.UserModel{
		Username:  req.Username,
		Email:     req.Email,
		Password:  string(passwordHash),
		CreatedAt: now,
		UpdatedAt: now,
	}

	// create user
	id, err := s.userRepo.CreateUser(ctx, userModel)
	if err != nil {
		return 0, http.StatusInternalServerError, err
	}

	return id, http.StatusCreated, nil
}
