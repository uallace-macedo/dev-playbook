# Playground

Laboratório de experimentos focado em validar comportamentos da runtime, sintaxe e fundamentos da linguagem Go.

## Tópicos

### [Closures](./closures/closures.go)
Estudo de funções anônimas e captura de escopo léxico (Lexical Scoping).
- **Specs:** Captura de variáveis por referência, State Isolation (Encapsulamento) e Function Factories.

## Como Executar

Cada subdiretório representa um pacote isolado. Para testar um conceito específico:

```bash
go run ./playground/nome-do-modulo