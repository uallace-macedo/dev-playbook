package config

import (
	"io"
	"log"
	"os"
)

type Logger struct {
	debug   *log.Logger
	info    *log.Logger
	warning *log.Logger
	err     *log.Logger
	writer  io.Writer
}

const (
	reset  = "\033[0m"
	red    = "\033[31m"
	green  = "\033[32m"
	yellow = "\033[33m"
	blue   = "\033[34m"
)

func NewLogger(p string) *Logger {
	writer := io.Writer(os.Stdout)
	logger := log.New(writer, p, log.Ldate|log.Ltime)

	return &Logger{
		debug:   log.New(log.Writer(), blue+"[DEBUG] "+reset, log.Flags()),
		info:    log.New(log.Writer(), green+"[INFO] "+reset, log.Flags()),
		warning: log.New(log.Writer(), yellow+"[WARNING] "+reset, log.Flags()),
		err:     log.New(log.Writer(), red+"[ERROR] "+reset, log.Flags()),
		writer:  logger.Writer(),
	}
}

func (l *Logger) Debug(v ...any) {
	l.debug.Println(v...)
}

func (l *Logger) Info(v ...any) {
	l.info.Println(v...)
}

func (l *Logger) Warning(v ...any) {
	l.warning.Println(v...)
}

func (l *Logger) Error(v ...any) {
	l.err.Println(v...)
}

func (l *Logger) Debugf(str string, v ...any) {
	l.debug.Printf(str, v...)
}

func (l *Logger) Infof(str string, v ...any) {
	l.info.Printf(str, v...)
}

func (l *Logger) Warningf(str string, v ...any) {
	l.warning.Printf(str, v...)
}

func (l *Logger) Errorf(str string, v ...any) {
	l.err.Printf(str, v...)
}
