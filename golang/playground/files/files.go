package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
)

type BotConfig struct {
	Token  string `json:"token"`
	Prefix string `json:"prefix"`
}

type ServerConfig struct {
	ConfigChannelID string `json:"config_channel_id"`
	FirstRoleID     string `json:"first_role_id"`
}

type Config struct {
	Name   string       `json:"name"`
	Bot    BotConfig    `json:"bot"`
	Server ServerConfig `json:"server"`
}

const configPath = "c.json"

func main() {
	cfg, err := loadConfig(configPath)
	if err != nil {
		log.Fatalf("Falha ao carregar configuração: %v", err)
	}

	cfg.Name = "JOOOHN"
	cfg.Server.FirstRoleID = "zero two"

	if err := saveConfig(configPath, cfg); err != nil {
		log.Fatalf("Falha ao salvar configuração: %v", err)
	}

	fmt.Printf("Configuração atualizada com sucesso: %+v\n", cfg)
}

func loadConfig(path string) (*Config, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var cfg Config
	if err := json.NewDecoder(file).Decode(&cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}

func saveConfig(path string, cfg *Config) error {
	bytes, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return err
	}

	tmpPath := path + ".tmp"
	if err := os.WriteFile(tmpPath, bytes, 0644); err != nil {
		return err
	}

	return os.Rename(tmpPath, path)
}
