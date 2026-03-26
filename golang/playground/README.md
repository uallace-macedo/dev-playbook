# Playground

Laboratório de experimentos focado em validar comportamentos da runtime, sintaxe e fundamentos da linguagem Go.

## Tópicos

### [Closures](./closures/closures.go)
Estudo de funções anônimas e captura de escopo léxico (Lexical Scoping).
- **Specs:** Captura de variáveis por referência, State Isolation (Encapsulamento) e Function Factories.

### [Pointers](./pointers/pointers.go)
Gerenciamento de endereços de memória e diferenciação entre passagem por valor e referência.
- **Specs:** Operadores `&` e `*`, Mutabilidade, e análise de Performance (Stack vs Heap).

### [Enums (Iota & String Types)](./enums/enums.go)
Simulação de tipos enumerados utilizando constantes tipadas.
- **Specs**: iota (Auto-increment), Stringer Interface para logs legíveis e segurança de tipos em assinaturas de funções.

### [Interfaces](./interfaces)
Implementação de polimorfismo via Satisfação Implícita (Duck Typing).
- **Specs:** Conjunto de métodos (Method Sets), Empty Interface (`interface{}` / `any`), Type Assertion e Type Switches.

## Como Executar

Cada subdiretório representa um pacote isolado. Para testar um conceito específico:

```bash
go run ./playground/nome-do-modulo