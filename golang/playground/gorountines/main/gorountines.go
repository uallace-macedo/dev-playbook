package main

import (
	"fmt"
	"gorountines/food"
	"sync"
)

type PizzaResponse struct {
	OrderID int
	Pizza   food.PizzaFlavor
}

func preparePizza(i int, p food.PizzaFlavor, w *sync.WaitGroup, c chan PizzaResponse) {
	defer w.Done()
	fmt.Printf("[👨‍🍳 KITCHEN] Cooking Order %d: %s...\n", i, p.String())
	c <- PizzaResponse{OrderID: i, Pizza: p}
}

func main() {
	menu := food.GetPizzaMenu()
	totalOrders := len(menu)

	pizzaChan := make(chan PizzaResponse, totalOrders)
	var wg sync.WaitGroup

	for i, flavor := range menu {
		wg.Add(1)
		go preparePizza(i, flavor, &wg, pizzaChan)
	}

	go func() {
		wg.Wait()
		close(pizzaChan)
	}()

	for res := range pizzaChan {
		fmt.Printf("[🍕 DELIVERY] Order %d is ready! Enjoy your %s\n", res.OrderID, res.Pizza)
	}

	fmt.Println(">>> 🔥 All pizzas have been delivered.")
}
