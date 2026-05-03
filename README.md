# Documento de Requisitos e Estrutura de Diretórios para o MVP "laboratorio-taskapi"

Este documento descreve os requisitos funcionais e não funcionais para o desenvolvimento do MVP "laboratorio-taskapi", uma Micro-API de To-Do List utilizando Python, FastAPI e SQLAlchemy. Como desenvolvedor iniciante em Python, foque em conceitos fundamentais como roteamento, validação de dados e interação com banco de dados. O objetivo é criar uma API simples e funcional que permita gerenciar tarefas (tasks) de forma básica.

## 1. Requisitos Funcionais (CRUD)

Os requisitos funcionais definem as operações básicas que a API deve suportar para gerenciar tarefas. Cada operação segue o padrão CRUD (Create, Read, Update, Delete) e será implementada como endpoints RESTful.

- **Criar Tarefa (Create)**:
  - Endpoint: `POST /tasks`
  - Descrição: Permite criar uma nova tarefa com título, descrição e status (ex.: "pendente", "em_progresso", "concluída").
  - Validação: Título obrigatório (mínimo 1 caractere, máximo 100); descrição opcional (máximo 500 caracteres); status padrão é "pendente".
  - Resposta: Retorna a tarefa criada com ID gerado automaticamente.

- **Listar Tarefas (Read - Listar Todas)**:
  - Endpoint: `GET /tasks`
  - Descrição: Retorna uma lista de todas as tarefas armazenadas, incluindo ID, título, descrição e status.
  - Filtros Opcionais: Suporte a filtros por status (ex.: `?status=pendente`, `?status=concluida`).
  - Paginação: Suporte a `skip` e `limit` para listar com offset.
  - Resposta: Lista de tarefas em formato JSON.

- **Obter Tarefa Específica (Read - Por ID)**:
  - Endpoint: `GET /tasks/{task_id}`
  - Descrição: Retorna os detalhes de uma tarefa específica pelo ID.
  - Validação: ID deve existir; caso contrário, retorna erro 404.
  - Resposta: Detalhes da tarefa em formato JSON.

- **Atualizar Tarefa (Update)**:
  - Endpoint: `PUT /tasks/{task_id}`
  - Descrição: Permite atualizar título, descrição ou status de uma tarefa existente.
  - Validação: ID deve existir; campos atualizados seguem as mesmas regras de criação.
  - Resposta: Retorna a tarefa atualizada.

- **Marcar Tarefa como Concluída (Partial Update)**:
  - Endpoint: `PATCH /tasks/{task_id}/complete`
  - Descrição: Marca uma tarefa como concluída atualizando seu status para "concluida".
  - Validação: ID deve existir; caso contrário, retorna erro 404.
  - Resposta: Retorna a tarefa com status atualizado.

- **Excluir Tarefa (Delete)**:
  - Endpoint: `DELETE /tasks/{task_id}`
  - Descrição: Remove uma tarefa pelo ID.
  - Validação: ID deve existir; caso contrário, retorna erro 404.
  - Resposta: Confirmação de exclusão (ex.: status 204 No Content).

Essas operações formam a base funcional da API, garantindo que usuários possam gerenciar tarefas de forma intuitiva. Implemente tratamento de erros para casos como IDs inválidos ou dados malformados.

## 2. Requisitos Não Funcionais

Os requisitos não funcionais especificam aspectos técnicos e de qualidade que suportam os funcionais, assegurando robustez, segurança e manutenibilidade.

- **Persistência de Dados**:
  - Utilize SQLite como banco de dados relacional para armazenar tarefas.
  - Configuração: Arquivo local (ex.: `tasks.db`) para simplicidade no MVP; SQLAlchemy como ORM para abstrair consultas SQL.
  - Migrações: Use Alembic (integrado ao SQLAlchemy) para gerenciar mudanças no esquema do banco.

- **Validação de Dados**:
  - Implemente validação usando Pydantic para esquemas de entrada e saída.
  - Regras: Campos obrigatórios, limites de tamanho, tipos de dados (ex.: string para título, enum para status).
  - Enumerações: Status deve ser um Enum com valores válidos: "pendente", "em_progresso", "concluida".
  - Tratamento de Erros: Retorne mensagens claras em caso de validação falhada (ex.: erro 422 Unprocessable Entity).

- **Segurança Básica**:
  - Autenticação: Não implementada no MVP (simplifique para foco no CRUD), mas prepare estrutura para futuras adições (ex.: JWT).
  - Validação de Entrada: Proteja contra injeção SQL via SQLAlchemy e sanitização de dados.

- **Performance e Escalabilidade**:
  - Tempo de Resposta: Mantenha endpoints rápidos (< 500ms) para operações básicas.
  - Limitação: Não aplicável no MVP, mas considere paginação para listagem de tarefas se o volume crescer.

- **Documentação e Testabilidade**:
  - Documentação Automática: Use FastAPI para gerar docs interativas via Swagger UI (acessível em `/docs`).
  - Testes Unitários: Implemente testes para modelos, esquemas, serviços e endpoints usando pytest.
  - Docstrings: Todos os módulos, classes e funções devem possuir docstrings descritivas.
  - Logs: Adicione logging simples para depuração (ex.: usando Python's `logging`).

- **Compatibilidade e Ambiente**:
  - Python Versão: 3.8+ para compatibilidade com FastAPI e SQLAlchemy.
  - Dependências: Liste em `requirements.txt` (ex.: `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`).
  - Ambiente: Suporte a execução local via virtualenv; prepare para deploy simples (ex.: via Uvicorn).

Esses requisitos garantem que a API seja confiável e fácil de manter, mesmo para iniciantes.

## 3. Estrutura de Diretórios Revisada

Para organizar o código de forma modular e escalável, adote a seguinte estrutura de pastas. Isso separa responsabilidades: modelos para o banco, esquemas para validação, rotas para endpoints, serviços para lógica de negócio e testes para validação.

```
laboratorio-taskapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação FastAPI
│   ├── database.py          # Configuração do banco de dados (SQLAlchemy engine/session)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Modelo SQLAlchemy para Task com enum de status
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Esquemas Pydantic para validação (TaskCreate, TaskUpdate, etc.)
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Lógica de negócio (CRUD, filtros, buscas)
│   └── routes/
│       ├── __init__.py
│       └── tasks.py         # Endpoints CRUD para tarefas com docstrings
├── alembic/                 # Diretório para migrações do banco
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── test_tasks.py        # Testes para endpoints
│   └── test_services.py     # Testes para serviços de negócio
├── requirements.txt         # Dependências Python
├── README.md                # Documentação do projeto (como executar, endpoints)
└── .gitignore               # Ignorar arquivos como __pycache__, *.db
```

- **Explicação da Estrutura**:
  - `app/`: Pasta principal do código, com subpastas para separação clara.
  - `models/`: Contém classes SQLAlchemy que representam tabelas do banco com Enums.
  - `schemas/`: Define esquemas Pydantic para entrada/saída de dados, garantindo validação.
  - `services/`: Camada de lógica de negócio, separada dos endpoints. Contém métodos para CRUD, filtros e buscas.
  - `routes/`: Agrupa os endpoints FastAPI, facilitando manutenção e documentação.
  - `alembic/`: Para migrações automáticas do banco.
  - `tests/`: Para testes unitários (endpoints e serviços).
  - Arquivos Raiz: `requirements.txt` para dependências; `README.md` para instruções.

Essa estrutura promove boas práticas em Python/FastAPI, facilitando expansão futura (ex.: adicionar autenticação, mais recursos ou endpoints). A camada de serviços separa a lógica de negócio dos endpoints, tornando o código mais testável e reutilizável.

## Instalação e Execução

### Instalação

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
4. Instale as dependências: `pip install -r requirements.txt`

### Execução

Execute o servidor: `uvicorn app.main:app --reload`

Acesse a documentação em: http://127.0.0.1:8000/docs

### Endpoints

#### Criar Tarefa
- **Método**: `POST /tasks`
- **Body**: `{"title": "Minha tarefa", "description": "Descrição", "status": "pendente"}`
- **Resposta**: Tarefa criada com ID

#### Listar Tarefas
- **Método**: `GET /tasks`
- **Parâmetros**: `?status=pendente&skip=0&limit=10`
- **Resposta**: Lista de tarefas

#### Obter Tarefa Específica
- **Método**: `GET /tasks/{id}`
- **Resposta**: Detalhes da tarefa

#### Atualizar Tarefa
- **Método**: `PUT /tasks/{id}`
- **Body**: `{"title": "Novo título", "description": "Nova descrição", "status": "em_progresso"}`
- **Resposta**: Tarefa atualizada

#### Marcar Tarefa como Concluída
- **Método**: `PATCH /tasks/{id}/complete`
- **Resposta**: Tarefa com status "concluida"

#### Excluir Tarefa
- **Método**: `DELETE /tasks/{id}`
- **Resposta**: Status 204 No Content

### Testes

Execute os testes:
```bash
pytest
```

Execute testes com cobertura:
```bash
pytest --cov=app
```

### Status das Tarefas

As tarefas suportam os seguintes status:
- `pendente`: Tarefa aguardando execução (padrão)
- `em_progresso`: Tarefa em execução
- `concluida`: Tarefa concluída
- `GET /tasks`: Listar tarefas
- `GET /tasks/{id}`: Obter tarefa por ID
- `PUT /tasks/{id}`: Atualizar tarefa
- `DELETE /tasks/{id}`: Excluir tarefa

## Testes

Execute os testes: `pytest`