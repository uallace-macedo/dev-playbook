# 🍔 VFDelivery — Desafio Food Delivery (Vecodes)

> ⚠️ **Status do Projeto:** 🚧 *Em desenvolvimento*.
> As funcionalidades básicas e a arquitetura estão sendo construídas de acordo com a documentação em `.docs/`.

---

## 📌 Sobre o Projeto

O **VFDelivery** é uma API REST desenvolvida para gerenciar o fluxo completo de pedidos de um sistema de Food Delivery, com foco principal no **gerenciamento de estados do pedido** (desde a criação até a avaliação pelo cliente) e na aplicação de regras de acesso granulares.

---

## 🛠️ Tech Stack & Arquitetura

- **Linguagem/Framework:** Python + FastAPI
- **Banco de Dados:** PostgreSQL
- **ORM & Migrações:** SQLAlchemy + Alembic
- **Conteinerização:** Docker + Docker Compose

---

## 📂 Documentação e Desenho da Solução

Toda a modelagem e o planejamento da solução estão detalhados na pasta `.docs/`:

* 🏛️ [**Arquitetura e Decisões Técnicas**](.docs/architecture.md)
* 📜 [**Regras de Negócio e Transições de Estado**](.docs/bussiness-rules.md)
* 🗄️ [**Modelo de Dados & Diagramas ER/Estados**](.docs/domain-models.md)

---

## 🔄 Fluxo e Ciclo de Vida do Pedido

O principal objetivo da aplicação é garantir a seguinte transição obrigatória de estados:

```text
[CREATED] ──► [ACCEPTED] ──► [DELIVERED] ──► [REVIEWED]
    │
    └──► [REJECTED]
```

### Principais Regras
1. **Atribuição:** Apenas o restaurante associado ao pedido pode **Aceitar** ou **Recusar**.
2. **Entrega:** Apenas pedidos no estado `ACCEPTED` podem ser marcados como `DELIVERED`.
3. **Avaliação:** Apenas o cliente autor do pedido pode enviar uma avaliação e apenas se o status for `DELIVERED`.
4. **Estados Finais:** Pedidos `REJECTED` entram em estado terminal e bloqueiam qualquer ação subsequente.

---

## 🚀 Como Executar o Projeto

*(Instruções em breve...)*

```bash
# Clone o repositório
git clone https://github.com/uallace-macedo/vfdelivery.git

# Suba a aplicação com Docker Compose
# docker compose up -d --build (Ainda não implementado.)
```

A documentação interativa da API estará disponível em `http://localhost:8000/docs` assim que o ambiente estiver ativo.

---
