package main

import (
	"fmt"
)

func main() {
	// 1. Criando a lista (Capacidade inicial: 5)
	minhaLista := NewArrayList[int]()
	fmt.Println("--- Teste de Inserção e Grow ---")

	// 2. Adicionando 6 itens (Isso vai disparar o grow no 6º item)
	for i := 1; i <= 6; i++ {
		minhaLista.Add(i * 10)
		fmt.Printf("Adicionado: %d | Tamanho Atual: %d\n", i*10, i)
	}

	// 3. Teste de Leitura (Get)
	val, err := minhaLista.Get(2) // Pega o 30
	if err == nil {
		fmt.Printf("\nItem no índice 2: %d\n", val)
	}

	// 4. Teste de Erro (Index out of bound)
	_, err = minhaLista.Get(10)
	if err != nil {
		fmt.Printf("Erro esperado: %v\n", err)
	}

	// 5. Teste de Remoção (Remove)
	fmt.Println("\n--- Teste de Remoção (Removendo o índice 1: valor 20) ---")
	minhaLista.Remove(1)

	// 6. Verificando como ficou a lista após o Shift
	fmt.Println("Lista após remover o 20:")
	for i := 0; i < 5; i++ { // O size agora é 5, mas vamos ler até o antigo limite
		v, _ := minhaLista.Get(i)
		fmt.Printf("Índice %d: %d\n", i, v)
	}
}
