# Diagramas de Arquitetura — laboratorio-taskapi

Este documento contém diagramas Mermaid representando a arquitetura do sistema FastAPI com camadas API, Service, Repository e o componente PriorityAdvisor.

## Diagrama de Fluxo de Dados

O diagrama abaixo ilustra o caminho de uma requisição HTTP desde o cliente até o banco de dados SQLite, passando pelas camadas da aplicação.

```mermaid
graph TD
    A[Cliente] --> B[FastAPI Router]
    B --> C[Service Layer]
    C --> D[Repository Layer]
    D --> E[SQLite Database]
    E --> D
    D --> C
    C --> B
    B --> A

    style A fill:#e1f5fe
    style B fill:#b3e5fc
    style C fill:#81d4fa
    style D fill:#4fc3f7
    style E fill:#29b6f6
```

### Lógica de Persistência
A lógica de persistência segue o padrão Repository: a camada Service coordena a lógica de negócio e delega operações de dados à Repository Layer, que utiliza SQLAlchemy para interagir com o SQLite. Dados são validados na entrada (API Layer via Pydantic), processados na Service Layer, persistidos na Repository Layer e retornados ao cliente. O PriorityAdvisor pode ser integrado na Service Layer para sugerir prioridades baseadas em regras de negócio.

## Diagrama de Componentes

O diagrama de componentes mostra as principais camadas e o componente PriorityAdvisor.

```mermaid
graph LR
    subgraph "API Layer"
        R[FastAPI Routers]
    end

    subgraph "Service Layer"
        S[TaskService]
        P[PriorityAdvisor]
    end

    subgraph "Repository Layer"
        M[SQLAlchemy Models]
    end

    subgraph "Database"
        DB[SQLite]
    end

    R --> S
    S --> P
    S --> M
    M --> DB

    style R fill:#e8f5e8
    style S fill:#c8e6c9
    style P fill:#a5d6a7
    style M fill:#81c784
    style DB fill:#66bb6a
```