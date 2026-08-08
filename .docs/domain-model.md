# 🗄️ Modelo de Dados e Estados

## Diagrama ER

```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : "cria"
  RESTAURANT ||--o{ ORDER : "recebe"
  RESTAURANT ||--o{ PRODUCT : "possui"
  PRODUCT ||--o{ ORDER : "está em"
  ORDER ||--o| REVIEW : "possui"

  CUSTOMER {
    string id PK "UUID"
    string name
    string email
  }

  RESTAURANT {
    string id PK "UUID"
    string name
    string email
  }

  PRODUCT {
    string id PK "UUID"
    string restaurant_id FK
    string name
    decimal price
  }

  ORDER {
    string id PK "UUID"
    string customer_id FK
    string restaurant_id FK
    string product_id FK
    int quantity "Quantidade do produto"
    string status "CREATED | ACCEPTED | REJECTED | DELIVERED | REVIEWED"
    decimal total_value "Calculado: price * quantity"
    datetime created_at
  }

  REVIEW {
    string id PK "UUID"
    string order_id FK "UQ"
    string customer_id FK
    int rating
    string comment
  }
```

## Ciclo de Vida do Pedido
```mermaid
stateDiagram-v2
  [*] --> CREATED
  CREATED --> ACCEPTED : Restaurante aceita
  CREATED --> REJECTED : Restaurante recusa
  ACCEPTED --> DELIVERED : Entrega confirmada
  DELIVERED --> REVIEWED : Cliente avalia
  REJECTED --> [*]
  REVIEWED --> [*]
```
