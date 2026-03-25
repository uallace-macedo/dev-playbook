package main

import "fmt"

type paymentGateway interface {
	pay(amount float32)
}

type payment struct {
	gateway paymentGateway
}

func (p payment) makePayment(amount float32) {
	p.gateway.pay(amount)
}

type pix struct{}

func (p pix) pay(amount float32) {
	fmt.Println("making payment using pix", amount)
}

type stripe struct{}

func (s stripe) pay(amount float32) {
	fmt.Println("making payment using stripe", amount)
}

func main() {
	stripePaymentGw := stripe{}
	pgw1 := payment{gateway: stripePaymentGw}
	pgw1.makePayment(100)

	pixPaymentGw := pix{}
	pgw2 := payment{gateway: pixPaymentGw}
	pgw2.makePayment(100)
}
