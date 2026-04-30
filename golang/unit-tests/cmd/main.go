package main

import (
	"log"

	"github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/database"
	"github.com/uallace-macedo/dev-playbook/golang/unit-tests/internal/http"
)

func main() {
	port := ":5000"
	db, err := database.NewConnection("postgres://user:password@localhost:4000/unit_tests_db?sslmode=disable")
	if err != nil {
		log.Fatal("could not connect to db")
	}

	http.StartServer(port, db)
}
