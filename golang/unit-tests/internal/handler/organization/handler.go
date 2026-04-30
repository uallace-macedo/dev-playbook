package organization

import (
	"github.com/labstack/echo/v4"
	repo "github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/repository/organization"
)

type (
	OrganizationHandler interface {
		FetchById(c echo.Context) error
	}

	organizationHandler struct {
		repo repo.OrganizationRepository
	}
)

func NewOrganizationHandler(repo repo.OrganizationRepository) *organizationHandler {
	return &organizationHandler{
		repo: repo,
	}
}
