# 📜 Regras de Negócio

## Regras de Transição e Acesso
1. **CREATED → ACCEPTED/REJECTED:** Apenas pelo **Restaurante** dono do pedido.
2. **ACCEPTED → DELIVERED:** Apenas pelo **Restaurante** dono do pedido.
3. **DELIVERED → REVIEWED:** Apenas pelo **Cliente** dono do pedido.
4. **REJECTED:** Estado terminal. Não aceita novas ações.
