package main

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
)

type api struct {
	addr string
}

var users = []User{}

func (a *api) getUsersHandler(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-type", "application/json")

	if err := json.NewEncoder(w).Encode(users); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func (a *api) createUsersHandler(w http.ResponseWriter, r *http.Request) {
	var payload User
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	u := User{
		FirstName: payload.FirstName,
		LastName:  payload.LastName,
	}

	if err := insertUser(u); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusCreated)
}

func insertUser(u User) error {
	if strings.TrimSpace(u.FirstName) == "" {
		return errors.New("first_name is required")
	}

	if strings.TrimSpace(u.LastName) == "" {
		return errors.New("last_name is required")
	}

	for _, user := range users {
		if user.FirstName == u.FirstName && user.LastName == u.LastName {
			return errors.New("user already exists")
		}
	}

	users = append(users, u)
	return nil
}
