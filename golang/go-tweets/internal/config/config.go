package config

import (
	"fmt"
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	DBUrlMigration string `json:"DATABASE_URL"`

	DBHost     string `json:"DB_HOST"`
	DBUser     string `json:"DB_USER"`
	DBPassword string `json:"DB_PASSWORD"`
	DBPort     string `json:"DB_PORT"`
	DBName     string `json:"DB_NAME"`

	APIPort      string `json:"API_PORT"`
	APISecretJWT string `json:"API_SECRET_JWT"`
}

func LoadConfig(l *Logger) (*Config, error) {
	if err := godotenv.Load(); err != nil {
		return nil, fmt.Errorf("Failed to load .env file\n")
	}

	l.Info("config loaded")

	return &Config{
		DBUrlMigration: os.Getenv("DATABASE_URL"),

		DBHost:     os.Getenv("DB_HOST"),
		DBUser:     os.Getenv("DB_USER"),
		DBPassword: os.Getenv("DB_PASSWORD"),
		DBPort:     os.Getenv("DB_PORT"),
		DBName:     os.Getenv("DB_NAME"),

		APIPort:      os.Getenv("API_PORT"),
		APISecretJWT: os.Getenv("API_SECRET_JWT"),
	}, nil
}
