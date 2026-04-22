package main

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/uallace-macedo/dev-playbook/golang/ratelimit_with_redis/internal/middleware"
)

func main() {
	c := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})
	defer c.Close()

	router := http.NewServeMux()
	rLMiddleware := middleware.NewRateLimiter(
		&middleware.RateLimiter{
			Client:  c,
			Limit:   3,
			Window:  10 * time.Second,
			Context: context.Background(),
		},
		router,
	)

	router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello, world!\n")
	})

	http.ListenAndServe(":8080", rLMiddleware)
}
