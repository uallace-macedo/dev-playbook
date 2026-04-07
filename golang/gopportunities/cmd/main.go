package main

import (
	"github.com/uallace-macedo/dev-playbook/golang/gopportunities/config"
	"github.com/uallace-macedo/dev-playbook/golang/gopportunities/router"
)

var (
	logger config.Logger
)

func main() {
	logger = *config.GetLogger("main")

	err := config.Init()
	if err != nil {
		logger.Errorf("config initialization error: %v\n", err)
		return
	}

	router.Initialize()
}
