# Diagramas de Arquitetura — laboratorio-taskapi

Este documento contém diagramas Mermaid representando a arquitetura do sistema FastAPI com camadas de Routes, Services, Schemas e Models para persistência em SQLite.

## Diagrama de Fluxo de Dados (Requisição HTTP)

O diagrama abaixo ilustra o caminho de uma requisição HTTP desde o cliente até o banco de dados SQLite, passando pelas camadas da aplicação conforme estrutura definida no projeto.

```mermaid
graph TD
    A[Cliente HTTP] -->|Request JSON| B[FastAPI Routes]
    B -->|Validação| C[Pydantic Schemas]
    C -->|Dados Validados| D[TaskService]
    D -->|SQL Queries| E[SQLAlchemy Models]
    E -->|Read/Write| F[SQLite Database]
    F -->|Resultado| E
    E -->|Objetos Task| D
    D -->|Task Objects| C
    C -->|Response JSON| B
    B -->|Response JSON| A

    style A fill:#e1f5fe
    style B fill:#b3e5fc
    style C fill:#81d4fa
    style D fill:#4fc3f7
    style E fill:#29b6f6
    style F fill:#1e88e5
```

### Fluxo de Persistência

1. **Request:** Cliente envia requisição HTTP com JSON
2. **Validação:** FastAPI Routes recebe e passa aos Schemas Pydantic para validação
3. **Processamento:** TaskService coordena lógica de negócio e chama modelos
4. **Persistência:** SQLAlchemy Models interagem com SQLite via ORM
5. **Resposta:** Dados retornam através das camadas em formato JSON validado

## Diagrama de Componentes

O diagrama de componentes mostra os pacotes do projeto e suas responsabilidades.

```mermaid
graph TB
    subgraph "app/routes"
        R["tasks.py<br/>(Endpoints CRUD)"]
    end

    subgraph "app/schemas"
        S["task.py<br/>(Pydantic Models)"]
    end

    subgraph "app/services"
        SVC["task_service.py<br/>(TaskService)"]
    end

    subgraph "app/models"
        M["task.py<br/>(SQLAlchemy Models)"]
    end

    subgraph "app/database"
        DB["database.py<br/>(Engine/Session)"]
    end

    subgraph "SQLite"
        DATA["tasks.db"]
    end

    R -->|Usa| S
    R -->|Chama| SVC
    SVC -->|Query| M
    M -->|Session| DB
    DB -->|Conecta| DATA

    style R fill:#e8f5e8
    style S fill:#c8e6c9
    style SVC fill:#a5d6a7
    style M fill:#81c784
    style DB fill:#66bb6a
    style DATA fill:#2e7d32
```

### Responsabilidades de Cada Camada

- **Routes** (`app/routes/tasks.py`): Define endpoints CRUD e delega para services
- **Schemas** (`app/schemas/task.py`): Validação de entrada/saída com Pydantic
- **Services** (`app/services/task_service.py`): Lógica de negócio (CRUD, filtros, paginação)
- **Models** (`app/models/task.py`): Entidades SQLAlchemy para mapeamento ORM
- **Database** (`app/database.py`): Configuração de engine e session SQLAlchemy

## Diagrama de Endpoints

O diagrama abaixo mostra os endpoints CRUD implementados no MVP.

```mermaid
graph LR
    subgraph "Task API Endpoints"
        POST["POST /tasks<br/>(Create)"]
        GET["GET /tasks<br/>(List)"]
        GETID["GET /tasks/{id}<br/>(Read)"]
        PUT["PUT /tasks/{id}<br/>(Update)"]
        PATCH["PATCH /tasks/{id}/complete<br/>(Complete)"]
        DELETE["DELETE /tasks/{id}<br/>(Delete)"]
        HEALTH["GET /health<br/>(Healthcheck)"]
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
    PATCH -.->|Success| S200
    DELETE -.->|Success| S204
    HEALTH -.->|Success| S200
    
    POST -.->|Error| S422
    GETID -.->|Error| S404
    PUT -.->|Error| S404
    PATCH -.->|Error| S404
    DELETE -.->|Error| S404

    style POST fill:#c8e6c9
    style GET fill:#a5d6a7
    style GETID fill:#81c784
    style PUT fill:#66bb6a
    style PATCH fill:#558b2f
    style DELETE fill:#f57c00
    style HEALTH fill:#0288d1
```