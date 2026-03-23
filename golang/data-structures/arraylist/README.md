# ArrayList (Dynamic Array)

Implementação manual de uma lista dinâmica utilizando **Generics** em Go para fins de estudo de gerenciamento de memória e estruturas de dados.

## Estrutura de Dados

A \`struct\` utiliza três campos principais para controle de memória:
- \`data []T\`: Buffer de memória (slice interno).
- \`size int\`: Quantidade real de elementos presentes na lista.
- \`capacity int\`: Tamanho total do espaço alocado no buffer.

## Complexidade Computacional

| Operação | Complexidade | Descrição |
| :--- | :--- | :--- |
| **Acesso (Get)** | O(1) | Acesso direto via índice. |
| **Inserção (Add)** | O(1)* | Inserção no final. *Amortizado devido ao redimensionamento. |
| **Remoção (Remove)** | O(n) | Requer o deslocamento (shift) dos elementos à direita. |
| **Redimensionamento**| O(n) | Alocação de novo array e cópia de todos os elementos. |

## Detalhes de Implementação

1. **Encapsulamento**: Estrutura privada (\`arrayList\`), instanciada via \`NewArrayList\` para garantir a capacidade inicial.
2. **Crescimento (Grow)**: Quando \`size == capacity\`, a capacidade é dobrada ($*2$) para minimizar a frequência de realocações.
3. **Gestão de Memória**: No método \`Remove\`, a posição excedente no final do array é zerada (\`var zero T\`) para evitar retenção de referências (Memory Leak).
4. **Bounds Check**: Validação de índices em \`Get\` e \`Remove\` para prevenir acessos a endereços de memória inválidos.