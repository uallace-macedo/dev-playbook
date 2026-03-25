# Spring Basic (Fundamentals & Exception Handling)

Implementação de uma API REST base para estudo de roteamento, extração de parâmetros de URL e padronização de respostas de erro utilizando **ControllerAdvice**.

## Estrutura de Comunicação

A API utiliza o padrão **Web MVC** para separação de responsabilidades e **Java Records** para garantir a imutabilidade dos DTOs (Data Transfer Objects).

| Recurso | Anotação | Descrição                                                |
| :--- | :--- |:---------------------------------------------------------|
| **Ponto de Entrada** | `@RestController` | Combina `@Controller` e `@ResponseBody`.                 |
| **Mapeamento Base** | `@RequestMapping` | Define o prefixo de rota para a classe.                  |
| **Parâmetro de URL** | `@PathVariable` | Extração de variáveis diretamente do path (ex: `/name`). |
| **Query String** | `@RequestParam` | Parâmetros nomeados na URL (ex: `?name=val`).            |
| **Global Handler** | `@RestControllerAdvice`| Interceptador global para captura de exceções.           |

## Detalhes de Implementação

1. **Records para DTOs**: Uso de `ExceptionResponse` e `Greeting` como records. Reduz o boilerplate de getters/setters e assegura que os dados de resposta sejam thread-safe e imutáveis.
2. **Desacoplamento de Erros**: As exceções residem no pacote `exception.custom`. O lançamento de erros de domínio (ex: `UnsupportedMathOperationException`) não exige tratamento explícito nos Controllers (Unchecked Exceptions).
3. **Centralização de Resposta**: O `GlobalExceptionHandler` intercepta falhas e as converte no schema padrão definido em `ExceptionResponse`, mantendo a consistência da API mesmo em cenários de erro 4xx ou 5xx.
4. **Camada de Serviço (DI)**: Introdução do `@Service` para isolar a lógica de negócio do Controller. A injeção é feita via `@Autowired`, permitindo que o Spring gerencie o Singleton da classe `PersonService`.

## Endpoints de Teste

### Operações Matemáticas
A API expõe as seguintes operações via `PathVariable`, aceitando strings que são validadas e convertidas internamente:

| Operação | Rota | Exemplo `curl` |
| :--- | :--- | :--- |
| **Soma** | `/sum/{x}/{y}` | `curl http://localhost:8080/sum/10/5` |
| **Subtração** | `/sub/{x}/{y}` | `curl http://localhost:8080/sub/20/8` |
| **Divisão** | `/div/{x}/{y}` | `curl http://localhost:8080/div/100/2` |
| **Multiplicação** | `/times/{x}/{y}` | `curl http://localhost:8080/times/5/5` |
| **Média** | `/avg/{x}/{y}` | `curl http://localhost:8080/avg/10/20` |
| **Raiz Quadrada** | `/sqrt/{x}` | `curl http://localhost:8080/sqrt/64` |

### Gerenciamento de Person (CRUD Mock)
Implementação de um CRUD básico utilizando `ArrayList` e `AtomicLong` para simular persistência.

| Operação | Verbo | Rota | Exemplo `curl`                                                                                     |
| :--- | :--- | :--- |:---------------------------------------------------------------------------------------------------|
| **Listar** | `GET` | `/person` | `curl localhost:8080/person`                                                                       |
| **Buscar** | `GET` | `/person/{id}` | `curl localhost:8080/person/1`                                                                     |
| **Criar** | `POST` | `/person` | `curl -X POST localhost:8080/person -H 'Content-Type: application/json' -d '{"firstName":"USER"}'` |

### Notas Técnicas:
- **Validação de Input**: O sistema utiliza um método helper `isNumeric(String)` baseado em Regex (`[-+]?[0-9]*\\.?[0-9]+`) para validar os paths antes da operação.
- **Injeção de Dependência**: O `PersonController` consome o `PersonService` via `@Autowired`, seguindo o princípio de inversão de controle.
- **POJO Beans**: A classe `Person` implementa `Serializable` para garantir compatibilidade com streams de dados Java.

## Como Executar

```bash
./mvnw spring-boot:run
```