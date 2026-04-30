package organization

import (
	"context"

	"github.com/georgysavva/scany/v2/pgxscan"
	"github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/model/organization"
)

func (r *organizationRepository) FetchById(ctx context.Context, id string) (*organization.OrganizationModel, error) {
	var org organization.OrganizationModel

	query := `SELECT id, name, created_at FROM organizations WHERE id = $1`
	if err := pgxscan.Get(ctx, r.db, &org, query, id); err != nil {
		return nil, err
	}

	return &org, nil
}
