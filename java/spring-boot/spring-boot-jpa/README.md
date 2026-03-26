# Spring Boot & JPA (Persistence & Data Mapping)

Implementação de uma API REST focada na camada de persistência, utilizando **Spring Data JPA** para abstração de banco de dados e **MySQL** como storage para armazenamento persistente de dados.

## Estrutura de Persistência

O projeto demonstra como realizar o mapeamento objeto-relacional (ORM) e a comunicação entre o Java e o banco de dados SQL.

| Recurso | Anotação | Descrição |
| :--- | :--- | :--- |
| **Entidade** | `@Entity` | Define a classe como uma tabela no banco de dados. |
| **Chave Primária** | `@Id` & `@GeneratedValue` | Configura a estratégia de auto-incremento (Identity). |
| **Mapeamento** | `@Column` | Customiza propriedades da coluna (nullability, nome, tamanho). |
| **Repositório** | `JpaRepository` | Interface que fornece operações CRUD completas e paginação pronta. |
| **Service Layer** | `@Service` | Concentra a lógica de negócio e as chamadas ao Repository. |

## Detalhes de Implementação

1. **Abstração com Spring Data**: Ao estender `JpaRepository<Person, Long>`, a aplicação elimina a necessidade de escrever queries SQL manuais para operações básicas (save, find, delete).
2. **Gerenciamento de Estado**: O uso de JPA permite que os objetos Java sejam sincronizados com o banco de dados de forma transparente através do Entity Manager do Hibernate.
3. **Tratamento de Exceções**: Caso um recurso solicitado por ID não exista, o sistema lança uma `ResourceNotFoundException`, que é capturada globalmente para retornar um erro amigável ao cliente.
4. **Injeção de Dependência**: O projeto utiliza `@Autowired` para desacoplar as camadas de Controller, Service e Repository, facilitando a manutenção.

## Endpoints de Teste

### Gerenciamento de Person (CRUD Completo)
As operações abaixo interagem diretamente com o banco de dados configurado.

| Operação | Verbo | Rota | Exemplo `curl` |
| :--- | :--- | :--- | :--- |
| **Listar Todos** | `GET` | `/person` | `curl localhost:8080/person` |
| **Buscar por ID** | `GET` | `/person/{id}` | `curl localhost:8080/person/1` |
| **Criar** | `POST` | `/person` | `curl -X POST localhost:8080/person -H 'Content-Type: application/json' -d '{"firstName":"Uallace", "lastName":"Macedo", "address":"Brasil", "gender":"Male"}'` |
| **Atualizar** | `PUT` | `/person` | `curl -X PUT localhost:8080/person -H 'Content-Type: application/json' -d '{"id":1, "firstName":"Novo Nome", "lastName":"Macedo", "address":"Brasil", "gender":"Male"}'` |
| **Deletar** | `DELETE` | `/person/{id}` | `curl -X DELETE localhost:8080/person/1` |

### Notas Técnicas:
- **Configuração de Database**: Verifique o arquivo `src/main/resources/application.properties` para configurar a URL, usuário e senha do seu MySQL.
- **Auto-DDL**: O Hibernate está configurado para gerenciar a criação/atualização das tabelas automaticamente conforme as entidades são modificadas.

## Como Executar

### 1. Subir o Banco de Dados
Na raiz do projeto (onde está o arquivo `docker-compose.yml`), execute:
```bash
docker-compose up -d
```

### 2. Rodar a Aplicação
Após o banco estar online, rode:
```bash
./mvnw spring-boot:run
```