package main

import "fmt"

func main() {
	lista := NewLlist[string]()

	fmt.Println("--- 1. Testando Inserções ---")
	lista.Add("B")
	lista.Add("C")

	lista.PushFront("A")

	lista.InsertAt(2, "INTERCALADO")
	lista.InsertAt(lista.Size(), "FIM")

	lista.Display()
	fmt.Printf("Tamanho atual: %d | Tail atual: %v\n\n", lista.Size(), lista.tail.value)

	fmt.Println("--- 2. Testando Remoções ---")

	lista.RemoveAt(0)
	fmt.Print("Removeu index 0 (A): ")
	lista.Display()

	lista.RemoveAt(1)
	fmt.Print("Removeu index 1 (INTERCALADO): ")
	lista.Display()

	lista.RemoveAt(lista.Size() - 1)
	fmt.Print("Removeu o último (FIM): ")
	lista.Display()

	fmt.Printf("Tamanho final: %d | Nova Tail: %v\n\n", lista.Size(), lista.tail.value)

	fmt.Println("--- 3. Testando Erros ---")
	err := lista.RemoveAt(10)
	if err != nil {
		fmt.Printf("Erro esperado capturado: %v\n", err)
	}
}
