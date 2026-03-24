# Singly Linked List (Lista Ligada Simples)

Implementação de uma lista encadeada utilizando **Generics** em Go para estudo de manipulação de ponteiros e alocação dinâmica de nós.

## Estrutura de Dados

A implementação utiliza duas structs para separar a lógica do nó da lógica de controle:
- \`llnode[T]\`: Representa o nó, contendo o valor (\`value\`) e o ponteiro para o próximo (\`next\`).
- \`llist[T]\`: Estrutura de controle com ponteiros para o início (\`head\`), fim (\`tail\`) e contador de tamanho (\`len\`).

## Complexidade Computacional

| Operação | Complexidade | Descrição |
| :--- | :--- | :--- |
| **Acesso (Get)** | O(n) | Requer percorrer a lista do início até o índice desejado. |
| **Inserção (Add)** | O(1) | Inserção no final garantida pelo ponteiro \`tail\`. |
| **Inserção (PushFront)**| O(1) | Inserção no início via ponteiro \`head\`. |
| **Remoção (RemoveAt)** | O(n) | Requer navegação até o nó anterior (\`index - 1\`). |

## Detalhes de Implementação

1. **Otimização de Cauda**: A manutenção do ponteiro \`tail\` permite que a operação \`Add\` (inserção no final) seja O(1), eliminando a necessidade de iterar a lista toda.
2. **Navegação Predecessora**: Operações em índices específicos utilizam a lógica \`index - 1\` para posicionar o ponteiro no nó anterior ao alvo, permitindo o reajuste seguro dos ponteiros.
3. **Casos de Borda**: Tratamento explícito para remoção do índice 0 e casos onde a lista se torna vazia, garantindo que \`head\` e \`tail\` sejam resetados para \`nil\`.
4. **Gerenciamento de Memória**: A remoção baseia-se na perda de referência do nó (\`before.next = before.next.next\`), permitindo que o Garbage Collector do Go limpe a memória automaticamente.
