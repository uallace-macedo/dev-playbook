package database

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
)

func NewConnection(connStr string) (*pgxpool.Pool, error) {
	ctx := context.Background()
	pool, err := pgxpool.New(ctx, connStr)
	if err != nil {
		return nil, fmt.Errorf("error while connecting to db: %v", err)
	}

	if err := pool.Ping(ctx); err != nil {
		return nil, err
	}

	return pool, err
}
