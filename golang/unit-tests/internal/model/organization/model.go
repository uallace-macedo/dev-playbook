package organization

import "time"

type OrganizationModel struct {
	ID        int32     `db:"id" json:"id"`
	Name      string    `db:"name" json:"name"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
}
