# 🍔 VFDelivery — Desafio Food Delivery (Vecodes)

> ⚠️ **Status do Projeto:** 
> - 🟢 **Backend / API:** Concluído e operacional via Docker.
> - 🚧 **Frontend:** Em andamento.

---

## 📌 Sobre o Projeto

O **VFDelivery** é uma API REST desenvolvida para gerenciar o fluxo completo de pedidos de um sistema de Food Delivery, com foco principal no **gerenciamento de estados do pedido** (desde a criação até a avaliação pelo cliente) e na aplicação de regras de acesso granulares.

---

## 🛠️ Tech Stack & Arquitetura

- **Linguagem/Framework:** Python 3.12 + FastAPI
- **Gerenciador de Pacotes:** `uv`
- **Banco de Dados:** PostgreSQL 16
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

## 🚀 Como Executar o Backend

Certifique-se de ter o **Docker** e o **Docker Compose** instalados na sua máquina.

### 1. Clonar o repositório
```bash
git clone https://github.com/uallace-macedo/vfdelivery.git
cd vfdelivery
```

### 2. Configurar variáveis de ambiente
Crie o arquivo `.env` na pasta da API (`apps/api/.env`):
```bash
cp apps/api/.env.example apps/api/.env
```

### 3. Subir os containers
Execute o Docker Compose a partir da raiz para compilar o container da API, subir o banco PostgreSQL e aplicar as migrações automaticamente:

```bash
docker compose up -d --build
```

> ⏳ A API aguardará automaticamente o container do banco ficar no status `healthy` antes de inicializar e rodar o `alembic upgrade head`.

---

## 📍 Acessando a API e Documentação

Com os containers em execução, a API estará acessível em:

* 🚀 **Documentação Interativa (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* 📖 **Documentação Alternativa (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* 🗄️ **Banco de Dados (PostgreSQL Externo):** `localhost:6000` (mapeado para a porta interna `5432`)
