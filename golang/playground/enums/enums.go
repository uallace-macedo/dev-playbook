package main

import "fmt"

/* type OrderStatus int
const (
	Received  OrderStatus = iota
	Confirmed OrderStatus = iota
	Prepared  OrderStatus = iota
	Delivered OrderStatus = iota
)

func (s OrderStatus) String() string {
	return [...]string{"received","confirmed","prepared","delivered"}[s]
}
*/

type OrderStatus string

const (
	Received  OrderStatus = "received"
	Confirmed OrderStatus = "confirmed"
	Prepared  OrderStatus = "prepared"
	Delivered OrderStatus = "delivered"
)

func changeOrderStatus(status OrderStatus) {
	fmt.Println("changing order status to", status)
}

func main() {
	changeOrderStatus(Received)
}
