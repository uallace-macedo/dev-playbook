# Native Mux Server

Implementação de servidor HTTP utilizando apenas a biblioteca padrão (`net/http`) do Go (v1.22+).

## Objetivo
O projeto foca no uso do `ServeMux` nativo para roteamento e manipulação de estado em memória (slices).
* Roteamento com verbos HTTP direto no Mux.
* Decodificação e codificação de JSON (`encoding/json`).
* Tratamento de erros e validação manual de campos.

## Tratamento de Erros
A API retorna códigos de status apropriados para cada falha:
- `400 Bad Request`: JSON malformado ou campos obrigatórios ausentes.
- `405 Method Not Allowed`: Uso de verbo HTTP não mapeado no endpoint.
- `500 Internal Server Error`: Falhas críticas na serialização de dados.

## Endpoints

| Método | Endpoint | Função |
| :--- | :--- | :--- |
| `GET` | `/users` | Retorna lista de usuários cadastrados |
| `POST` | `/users` | Valida e insere um novo usuário no slice |

## Uso (cURL)

### Criar Usuário
```bash
curl -X POST http://localhost:8080/users -d '{"first_name": "Tyler", "last_name": "Durden"}'
```

### Listar Usuários
```bash
curl http://localhost:8080/users
```