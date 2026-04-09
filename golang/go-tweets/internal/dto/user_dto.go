package dto

type (
	RegisterRequest struct {
		Email          string `json:"email"`
		Username       string `json:"username"`
		Password       string `json:"password"`
		PasswordConfig string `json:"password_confirm"`
	}

	RegisterResponse struct {
		ID int64
	}
)
