package food

type PizzaFlavor int

const (
	Mozzarella PizzaFlavor = iota
	Pepperoni
	Marguerita
	ChickenWithCatupiry
)

func (i PizzaFlavor) String() string {
	return [...]string{"mozzarella", "pepperoni", "marguerita", "chicken with catupiry"}[i]
}

func GetPizzaMenu() []PizzaFlavor {
	return []PizzaFlavor{Mozzarella, Pepperoni, Marguerita, ChickenWithCatupiry}
}
