# Testes

Este documento descreve como configurar, gerar e executar os testes unitários

## 🛠️ Pré-requisitos

Antes de começar, você precisará ter instalado:
- Go (v1.21+)
- Mockgen (para testes unitários)

### Instalando o Mockgen

O mockgen é usado para simular nosso repositório de banco de dados.

```bash
go install go.uber.org/mock/mockgen@latest
```

*Certifique-se de que o seu $GOPATH/bin está no seu $PATH.*

## 🏗️ Estrutura de Testes

**1. Gerando os mocks**
    Nós utilizamos interfaces para permitir a criação de mocks. No topo de cada interface de repositório, existe o comando go:generate.

    Para atualizar ou criar novos mocks:

  ```bash
  mockgen -source=internal/repository/org_repo.go -destination=internal/mocks/mock_repo.go -package=mocks
  ```

**2. Table-Driven Tests**
    Nossos testes seguem o padrão Table-Driven Tests, o que facilita a adição de novos cenários de teste sem duplicar código.

    Exemplo de Cenário:

  ```go
  testCases := []struct {
    name           string
    id             string
    setupMocks     func()
    expectedStatus int
    expectError    bool
  }{
    {
      name: "sucesso ao buscar organização",
      id:   "123",
      setupMocks: func() {
        repositoryMock.EXPECT().
          FetchById(gomock.Any(), "123").
          Return(&model.Organization{}, nil)
      },
      expectedStatus: http.StatusOK,
      expectError:    false,
    },
  }
  ```

## 🚀 Como Executar

### Testes Unitários (Mocks)

Roda os testes de lógica sem precisar de banco de dados:

```bash
go test ./internal/organization/...
```

### Verificando Coverage (Cobertura)

Para garantir que 100% das linhas do seu Handler foram testadas (incluindo os retornos de erro):

```bash
go test ./internal/organization/...
```