# Playground

Laboratório de experimentos focado em validar comportamentos da runtime, sintaxe e fundamentos da linguagem Go.

## Tópicos

### [Closures](./closures/closures.go)
Estudo de funções anônimas e captura de escopo léxico (Lexical Scoping).
- **Specs:** Captura de variáveis por referência, State Isolation (Encapsulamento) e Function Factories.

### [Generics](./generics/generics.go)
Implementação de algoritmos e estruturas de dados independentes de tipo.
- **Specs:** Type Parameters ([T any]), Type Constraints e Generic Structs (Pilhas/Filas).

### [Pointers](./pointers/pointers.go)
Gerenciamento de endereços de memória e diferenciação entre passagem por valor e referência.
- **Specs:** Operadores `&` e `*`, Mutabilidade, e análise de Performance (Stack vs Heap).

### [Enums (Iota & String Types)](./enums/enums.go)
Simulação de tipos enumerados utilizando constantes tipadas.
- **Specs**: iota (Auto-increment), Stringer Interface para logs legíveis e segurança de tipos em assinaturas de funções.

### [Interfaces](./interfaces)
Implementação de polimorfismo via Satisfação Implícita (Duck Typing).
- **Specs:** Conjunto de métodos (Method Sets), Empty Interface (`interface{}` / `any`), Type Assertion e Type Switches.

### [Gorountines & Channels](./gorountines/main/gorountines.go)
Orquestração de concorrência e processamento assíncrono em pipelines de dados.
- **Specs:** sync.WaitGroup para sincronização de vida, Buffered Channels para comunicação entre produtores/consumidores e for range em canais para encerramento determinístico.

## Como Executar

Cada subdiretório representa um pacote isolado. Para testar um conceito específico:

```bash
go run ./playground/nome-do-modulo