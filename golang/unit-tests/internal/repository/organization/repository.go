package organization

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/model/organization"
)

type (
	OrganizationRepository interface {
		FetchById(ct context.Context, id string) (*organization.OrganizationModel, error)
	}

	organizationRepository struct {
		db *pgxpool.Pool
	}
)

func NewOrganizationRepository(db *pgxpool.Pool) *organizationRepository {
	return &organizationRepository{
		db: db,
	}
}
