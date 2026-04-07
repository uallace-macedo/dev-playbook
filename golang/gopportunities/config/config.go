package config

import (
	"errors"
)

func Init() error {
	return errors.New("fake error")
}

func GetLogger(p string) *Logger {
	logger := NewLogger(p)
	return logger
}
