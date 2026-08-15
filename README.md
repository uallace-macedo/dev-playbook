# 🍔 VFDelivery

Sistema de Food Delivery com foco no gerenciamento do fluxo de pedidos e controle de acesso por perfil.

---

## 📌 Status do Projeto

* **Backend / API:** Concluído (`http://localhost:8000`)
* **Frontend:** Concluído (`http://localhost`)

---

## 🛠️ Tech Stack

* **Backend:** Python 3.12, FastAPI, SQLAlchemy, Alembic, `uv`
* **Frontend:** React 19, Vite, TailwindCSS, React Hook Form, Nginx
* **Banco de Dados:** PostgreSQL 16
* **Infraestrutura:** Docker, Docker Compose

---

## 📂 Documentação

Planejamento e regras do sistema disponíveis em `.docs/`:

* 🏛️ [**Arquitetura**](.docs/architecture.md)
* 📜 [**Regras de Negócio**](.docs/bussiness-rules.md)
* 🗄️ [**Modelo de Dados**](.docs/domain-models.md)

---

## 🔄 Fluxo do Pedido

'''text
[CREATED] ──► [ACCEPTED] ──► [DELIVERED] ──► [REVIEWED]
    │
    └──► [REJECTED]
'''

---

## 🚀 Como Executar

### 1. Clonar o repositório
'''bash
git clone https://github.com/uallace-macedo/vfdelivery.git
cd vfdelivery
'''

### 2. Configurar o `.env`
'''bash
cp .env.example .env
'''

### 3. Subir com Docker
'''bash
docker compose up -d --build
'''

---

## 📍 Serviços e Endereços

* 🌐 **Frontend:** [http://localhost](http://localhost)
* 🚀 **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* 📖 **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* 🗄️ **PostgreSQL:** `localhost:6000`
