package http

import (
	"log"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/labstack/echo/v4"
	hand "github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/handler/organization"
	repo "github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/repository/organization"
)

func StartServer(port string, db *pgxpool.Pool) {
	e := echo.New()

	setupRoutes(e, db)
	log.Fatal(e.Start(port))
}

func setupRoutes(e *echo.Echo, db *pgxpool.Pool) {
	ogrRepo := repo.NewOrganizationRepository(db)
	ogrHand := hand.NewOrganizationHandler(ogrRepo)

	e.GET("/organization/:id", ogrHand.FetchById)
}
