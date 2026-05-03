# Diagramas de Arquitetura — laboratorio-taskapi

Este documento contém diagramas Mermaid da arquitetura atual do MVP: uma API FastAPI de tarefas com repositório em memória e sugestão de prioridade via `PriorityAdvisor`.

## Fluxo de Dados

O diagrama abaixo mostra o caminho de uma requisição HTTP desde o cliente até o repositório em memória.

```mermaid
graph TD
    A[Cliente HTTP] -->|Request JSON| B[FastAPI App<br/>app/main.py]
    B -->|Roteamento| C[Task Router<br/>app/api/task_routes.py]
    C -->|Validação e serialização| D[Schemas Pydantic<br/>app/models/task.py]
    C -->|Payload validado| E[TaskService<br/>app/services/task_service.py]
    E -->|title + description| F[PriorityAdvisor<br/>app/services/priority_advisor.py]
    F -->|priority_suggestion| E
    E -->|CRUD| G[TaskRepository<br/>app/repositories/task_repository.py]
    G -->|Read/Write| H[(Memória do processo)]
    H -->|TaskOut| G
    G -->|TaskOut| E
    E -->|TaskOut| C
    C -->|Response JSON| A

    style A fill:#e1f5fe
    style B fill:#b3e5fc
    style C fill:#81d4fa
    style D fill:#4fc3f7
    style E fill:#29b6f6
    style F fill:#ff9800
    style G fill:#0288d1
    style H fill:#01579b,color:#ffffff
```

### Etapas

1. O cliente envia uma requisição HTTP para a API.
2. `app/main.py` recebe a requisição e encaminha para o router registrado.
3. `app/api/task_routes.py` valida entrada e saída usando schemas Pydantic.
4. `TaskService` orquestra a regra de negócio.
5. `PriorityAdvisor` sugere prioridade ao criar tarefa ou ao atualizar título/descrição.
6. `TaskRepository` grava, consulta, atualiza ou remove tarefas em memória.
7. A resposta retorna ao cliente como JSON.

## Diagrama de Componentes

```mermaid
graph TB
    subgraph "Cliente"
        CLI["HTTP Client<br/>(curl, Postman, TestClient)"]
    end

    subgraph "FastAPI Application"
        APP["main.py<br/>(FastAPI app)"]
        ROUTER["api/task_routes.py<br/>(Task endpoints)"]
    end

    subgraph "Domain Models"
        MODELS["models/task.py<br/>(Enums + Pydantic schemas)"]
    end

    subgraph "Service Layer"
        SVC["services/task_service.py<br/>(TaskService)"]
        PA["services/priority_advisor.py<br/>(PriorityAdvisor)"]
    end

    subgraph "Repository Layer"
        REPO["repositories/task_repository.py<br/>(TaskRepository)"]
        STORE[("In-memory storage<br/>dict[int, TaskOut]")]
    end

    CLI -->|HTTP Request| APP
    APP -->|include_router| ROUTER
    ROUTER -->|Validates request/response| MODELS
    ROUTER -->|Calls service| SVC
    SVC -->|Suggest priority| PA
    PA -->|Priority| SVC
    SVC -->|CRUD operations| REPO
    REPO -->|Read/Write| STORE
    STORE -->|TaskOut| REPO
    REPO -->|TaskOut/list[TaskOut]| SVC
    SVC -->|Result| ROUTER
    ROUTER -->|HTTP Response| APP
    APP -->|JSON Response| CLI

    style CLI fill:#e1f5fe
    style APP fill:#b3e5fc
    style ROUTER fill:#81d4fa
    style MODELS fill:#4fc3f7
    style SVC fill:#29b6f6
    style PA fill:#ff9800
    style REPO fill:#0288d1
    style STORE fill:#01579b,color:#ffffff
```

### Responsabilidades

- **FastAPI App** (`app/main.py`): cria a aplicação, registra routers e expõe o healthcheck.
- **API Layer** (`app/api/task_routes.py`): implementa endpoints HTTP, status codes e tratamento de `404`.
- **Models** (`app/models/task.py`): define `TaskStatus`, `Priority`, `TaskCreate`, `TaskUpdate` e `TaskOut`.
- **Service Layer** (`app/services/task_service.py`): concentra a regra de negócio e coordena advisor/repositório.
- **PriorityAdvisor** (`app/services/priority_advisor.py`): sugere prioridade via LLM opcional ou heurística local.
- **Repository Layer** (`app/repositories/task_repository.py`): mantém tarefas em memória durante o ciclo de vida do processo.

## Diagrama de Endpoints

```mermaid
graph LR
    subgraph "Task API Endpoints"
        POST["POST /tasks/<br/>Create"]
        GET["GET /tasks/<br/>List"]
        GETID["GET /tasks/{task_id}<br/>Read"]
        PUT["PUT /tasks/{task_id}<br/>Update"]
        DELETE["DELETE /tasks/{task_id}<br/>Delete"]
        HEALTH["GET /health<br/>Healthcheck"]
    end

    subgraph "HTTP Status"
        S201["201 Created"]
        S200["200 OK"]
        S204["204 No Content"]
        S404["404 Not Found"]
        S422["422 Validation Error"]
    end

    POST -.->|Success| S201
    GET -.->|Success| S200
    GETID -.->|Success| S200
    PUT -.->|Success| S200
    DELETE -.->|Success| S204
    HEALTH -.->|Success| S200

    POST -.->|Invalid payload| S422
    PUT -.->|Invalid payload| S422
    GETID -.->|Missing task| S404
    PUT -.->|Missing task| S404
    DELETE -.->|Missing task| S404

    style POST fill:#ff9800
    style GET fill:#a5d6a7
    style GETID fill:#81c784
    style PUT fill:#66bb6a
    style DELETE fill:#f57c00
    style HEALTH fill:#0288d1,color:#ffffff
```

## Fluxo do PriorityAdvisor

```mermaid
sequenceDiagram
    participant Client as Cliente HTTP
    participant Router as task_routes.py
    participant Service as TaskService
    participant Advisor as PriorityAdvisor
    participant Repo as TaskRepository

    Client->>Router: POST /tasks/
    Router->>Service: create_task(TaskCreate)
    Service->>Advisor: analyze_task(title, description)
    alt OPENAI_API_KEY configurada e chamada externa disponível
        Advisor-->>Service: prioridade sugerida por LLM
    else Sem chave, biblioteca ausente, erro ou timeout
        Advisor-->>Service: prioridade sugerida por heurística local
    end
    Service->>Repo: create(payload, priority_suggestion)
    Repo-->>Service: TaskOut
    Service-->>Router: TaskOut
    Router-->>Client: 201 Created
```

### Regras de Heurística Local

| Prioridade | Palavras-chave |
| --- | --- |
| `crítica` | `urgente`, `agora`, `imediato`, `crítico`, `crítica`, `bloqueio` |
| `alta` | `atraso`, `importante`, `alta prioridade`, `alta` |
| `média` | `melhoria`, `refator`, `refatoração`, `documentação`, `ajuste`, `revisão` |
| `baixa` | Padrão quando nenhuma palavra-chave é encontrada. |

## Observações

- A persistência é em memória; os dados são perdidos ao reiniciar a aplicação.
- Não há banco de dados, SQLAlchemy ou Alembic no fluxo atual.
- Não existe endpoint `PATCH /tasks/{task_id}/complete` no router atual.
- A chamada externa do `PriorityAdvisor` é opcional e sempre possui fallback local.
