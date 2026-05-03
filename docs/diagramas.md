# Diagramas de Arquitetura — laboratorio-taskapi

Este documento contém diagramas Mermaid representando a arquitetura do sistema FastAPI com camadas API, Service, Repository e o componente de Priorização (PriorityAdvisor).

## Diagrama de Fluxo de Dados (Requisição HTTP)

O diagrama abaixo ilustra o caminho de uma requisição HTTP desde o cliente até o banco de dados SQLite, passando pelas camadas da aplicação.

```mermaid
graph TD
    A[Cliente HTTP] -->|Request JSON| B[FastAPI Routes]
    B -->|Validação| C[Pydantic Schemas]
    C -->|Dados Validados| D[TaskService]
    D -->|Consulta Prioridade| E[PriorityAdvisor]
    E -->|Sugestão Prioridade| D
    D -->|CRUD Operations| F[Repository Layer]
    F -->|SQL Queries| G[SQLAlchemy Models]
    G -->|Read/Write| H[SQLite Database]
    H -->|Resultado| G
    G -->|Objetos Task| F
    F -->|Task Objects| D
    D -->|Task Objects| C
    C -->|Response JSON| B
    B -->|Response JSON| A

    style A fill:#e1f5fe
    style B fill:#b3e5fc
    style C fill:#81d4fa
    style D fill:#4fc3f7
    style E fill:#ff6f00
    style F fill:#29b6f6
    style G fill:#1e88e5
    style H fill:#0d47a1
```

### Fluxo de Persistência

1. **Request:** Cliente envia requisição HTTP com JSON
2. **Validação:** FastAPI Routes recebe e passa aos Schemas Pydantic para validação
3. **Processamento:** TaskService coordena lógica de negócio e consulta PriorityAdvisor
4. **Priorização:** PriorityAdvisor retorna sugestão de prioridade baseada em regras
5. **Persistência:** Repository Layer executa operações CRUD via SQLAlchemy Models
6. **Banco de Dados:** SQLite persiste dados
7. **Resposta:** Dados retornam através das camadas em formato JSON validado

## Diagrama de Componentes

O diagrama de componentes mostra as camadas arquiteturais: Cliente, API Layer, Service Layer, PriorityAdvisor e Repository Layer.

```mermaid
graph TB
    subgraph "Cliente"
        CLI["HTTP Client<br/>(curl, Postman, etc)"]
    end

    subgraph "API Layer"
        R["routes/tasks.py<br/>(FastAPI Endpoints)"]
        S["schemas/task.py<br/>(Pydantic Models)"]
    end

    subgraph "Service Layer"
        SVC["services/task_service.py<br/>(TaskService)"]
    end

    subgraph "PriorityAdvisor Component"
        PA["advisors/priority.py<br/>(PriorityAdvisor)"]
    end

    subgraph "Repository Layer"
        REPO["repositories/task_repository.py<br/>(TaskRepository)"]
        M["models/task.py<br/>(SQLAlchemy Models)"]
    end

    subgraph "Persistence"
        DB["database.py<br/>(Engine/Session)"]
        DATA["SQLite Database<br/>(tasks.db)"]
    end

    CLI -->|HTTP Request| R
    R -->|Validação| S
    R -->|Coordenação| SVC
    SVC -->|Consulta| PA
    PA -->|Sugestão| SVC
    SVC -->|CRUD| REPO
    REPO -->|Query| M
    M -->|Session| DB
    DB -->|Connect| DATA
    DATA -->|Result| DB
    DB -->|Session| M
    M -->|Objects| REPO
    REPO -->|Entities| SVC
    SVC -->|Data| S
    S -->|Response| R
    R -->|HTTP Response| CLI

    style CLI fill:#e1f5fe
    style R fill:#b3e5fc
    style S fill:#81d4fa
    style SVC fill:#4fc3f7
    style PA fill:#ff6f00
    style REPO fill:#29b6f6
    style M fill:#1e88e5
    style DB fill:#0d47a1
    style DATA fill:#01579b
```

### Responsabilidades de Cada Camada

- **API Layer** (`routes/`, `schemas/`): Recebe requisições HTTP, valida com Pydantic e coordena com serviços
- **Service Layer** (`services/task_service.py`): Orquestra lógica de negócio, filtros, paginação e consulta PriorityAdvisor
- **PriorityAdvisor** (`advisors/priority.py`): Componente de priorização que sugere prioridades baseado em regras de negócio
- **Repository Layer** (`repositories/task_repository.py`): Abstrai operações CRUD e gerencia persistência
- **Models** (`models/task.py`): Entidades SQLAlchemy para mapeamento ORM
- **Database** (`database.py`): Configuração de engine e session SQLAlchemy

## Diagrama de Endpoints

O diagrama abaixo mostra os endpoints CRUD implementados no MVP com suporte a PriorityAdvisor.

```mermaid
graph LR
    subgraph "Task API Endpoints"
        POST["POST /tasks<br/>(Create com Prioridade)"]
        GET["GET /tasks<br/>(List com Filtros)"]
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

    style POST fill:#ff9800
    style GET fill:#a5d6a7
    style GETID fill:#81c784
    style PUT fill:#66bb6a
    style PATCH fill:#558b2f
    style DELETE fill:#f57c00
    style HEALTH fill:#0288d1
```

### Integração com PriorityAdvisor

O endpoint `POST /tasks` é enriquecido pelo **PriorityAdvisor**, que:
- Analisa título, descrição e contexto da tarefa
- Retorna sugestão de prioridade (baixa, média, alta, crítica)
- A prioridade sugerida é retornada na resposta para o cliente validar