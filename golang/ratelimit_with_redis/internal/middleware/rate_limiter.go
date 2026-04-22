package middleware

import (
	"context"
	"net"
	"net/http"
	"time"

	"github.com/go-redis/redis/v8"
)

type RateLimiter struct {
	Client  *redis.Client
	Limit   int
	Window  time.Duration
	Context context.Context
}

func NewRateLimiter(rL *RateLimiter, handler http.Handler) http.Handler {
	return rL.rateLimiterMiddleware(handler)
}

func (rL *RateLimiter) allow(key string) bool {
	pipe := rL.Client.Pipeline()

	incr := pipe.Incr(rL.Context, key)
	ttl := pipe.TTL(rL.Context, key)

	if _, err := pipe.Exec(rL.Context); err != nil {
		return true
	}

	if ttl.Val() < 0 {
		rL.Client.Expire(rL.Context, key, rL.Window)
	}

	return incr.Val() <= int64(rL.Limit)
}

func (rL *RateLimiter) rateLimiterMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cIP, _, _ := net.SplitHostPort(r.RemoteAddr)
		if !rL.allow(cIP) {
			http.Error(w, "too many requests", http.StatusTooManyRequests)
			return
		}

		next.ServeHTTP(w, r)
	})
}
