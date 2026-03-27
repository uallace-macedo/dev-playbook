package main

import (
	"fmt"
	"sync"
)

type post struct {
	views int
	mu    sync.Mutex
}

func (p *post) inc(w *sync.WaitGroup) {
	defer w.Done()
	p.mu.Lock()
	p.views++
	p.mu.Unlock()
}

func main() {
	var wg sync.WaitGroup
	myPost := post{views: 0}

	for range 100 {
		wg.Add(1)
		go myPost.inc(&wg)
	}

	wg.Wait()
	fmt.Println(myPost.views)
}
