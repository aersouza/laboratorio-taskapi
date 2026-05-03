# Documento de Requisitos e Estrutura de Diretórios para o MVP "laboratorio-taskapi"

Este documento descreve os requisitos funcionais e não funcionais para o desenvolvimento do MVP "laboratorio-taskapi", uma Micro-API de To-Do List utilizando Python, FastAPI e SQLAlchemy. Como desenvolvedor iniciante em Python, foque em conceitos fundamentais como roteamento, validação de dados e interação com banco de dados. O objetivo é criar uma API simples e funcional que permita gerenciar tarefas (tasks) de forma básica.

## 1. Requisitos Funcionais (CRUD)

Os requisitos funcionais definem as operações básicas que a API deve suportar para gerenciar tarefas. Cada operação segue o padrão CRUD (Create, Read, Update, Delete) e será implementada como endpoints RESTful.

- **Criar Tarefa (Create)**:
  - Endpoint: `POST /tasks`
  - Descrição: Permite criar uma nova tarefa com título, descrição e status (ex.: "pendente", "concluída").
  - Validação: Título obrigatório (mínimo 1 caractere, máximo 100); descrição opcional (máximo 500 caracteres); status deve ser um valor pré-definido.
  - Resposta: Retorna a tarefa criada com ID gerado automaticamente.

- **Listar Tarefas (Read - Listar Todas)**:
  - Endpoint: `GET /tasks`
  - Descrição: Retorna uma lista de todas as tarefas armazenadas, incluindo ID, título, descrição e status.
  - Filtros Opcionais: Suporte a filtros por status (ex.: `?status=pendente`).
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
  - Tratamento de Erros: Retorne mensagens claras em caso de validação falhada (ex.: erro 422 Unprocessable Entity).

- **Segurança Básica**:
  - Autenticação: Não implementada no MVP (simplifique para foco no CRUD), mas prepare estrutura para futuras adições (ex.: JWT).
  - Validação de Entrada: Proteja contra injeção SQL via SQLAlchemy e sanitização de dados.

- **Performance e Escalabilidade**:
  - Tempo de Resposta: Mantenha endpoints rápidos (< 500ms) para operações básicas.
  - Limitação: Não aplicável no MVP, mas considere paginação para listagem de tarefas se o volume crescer.

- **Documentação e Testabilidade**:
  - Documentação Automática: Use FastAPI para gerar docs interativas via Swagger UI (acessível em `/docs`).
  - Testes: Implemente testes unitários básicos com pytest para modelos e endpoints.
  - Logs: Adicione logging simples para depuração (ex.: usando Python's `logging`).

- **Compatibilidade e Ambiente**:
  - Python Versão: 3.8+ para compatibilidade com FastAPI e SQLAlchemy.
  - Dependências: Liste em `requirements.txt` (ex.: `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`).
  - Ambiente: Suporte a execução local via virtualenv; prepare para deploy simples (ex.: via Uvicorn).

Esses requisitos garantem que a API seja confiável e fácil de manter, mesmo para iniciantes.

## 3. Estrutura de Diretórios Sugerida

Para organizar o código de forma modular e escalável, adote a seguinte estrutura de pastas. Isso separa responsabilidades: modelos para o banco, esquemas para validação, rotas para endpoints e configuração para setup.

```
laboratorio-taskapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação FastAPI
│   ├── database.py          # Configuração do banco de dados (SQLAlchemy engine/session)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Modelo SQLAlchemy para Task
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Esquemas Pydantic para validação (TaskCreate, TaskUpdate, etc.)
│   └── routes/
│       ├── __init__.py
│       └── tasks.py         # Endpoints CRUD para tarefas
├── alembic/                 # Diretório para migrações do banco (gerado por Alembic)
│   ├── versions/
│   └── env.py
├── tests/
│   ├── __init__.py
│   └── test_tasks.py        # Testes para endpoints e modelos
├── requirements.txt         # Dependências Python
├── README.md                # Documentação do projeto (como executar, endpoints)
└── .gitignore               # Ignorar arquivos como __pycache__, *.db
```

- **Explicação da Estrutura**:
  - `app/`: Pasta principal do código, com subpastas para separação clara.
  - `models/`: Contém classes SQLAlchemy que representam tabelas do banco.
  - `schemas/`: Define esquemas Pydantic para entrada/saída de dados, garantindo validação.
  - `routes/`: Agrupa os endpoints FastAPI, facilitando manutenção.
  - `alembic/`: Para migrações automáticas do banco.
  - `tests/`: Para testes, essenciais para validar o CRUD.
  - Arquivos Raiz: `requirements.txt` para dependências; `README.md` para instruções.

Essa estrutura promove boas práticas em Python/FastAPI, facilitando expansão futura (ex.: adicionar autenticação ou mais recursos). Comece criando os arquivos passo a passo, testando cada endpoint incrementalmente. Se precisar de código de exemplo para implementação, consulte a documentação oficial do FastAPI e SQLAlchemy. Boa sorte no desenvolvimento!

## Instalação e Execução

### Instalação

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`

### Execução

Execute o servidor: `uvicorn app.main:app --reload`

Acesse a documentação em: http://127.0.0.1:8000/docs

### Endpoints

- `POST /tasks`: Criar tarefa
- `GET /tasks`: Listar tarefas
- `GET /tasks/{id}`: Obter tarefa por ID
- `PUT /tasks/{id}`: Atualizar tarefa
- `DELETE /tasks/{id}`: Excluir tarefa

### Testes

Execute os testes: `pytest`
- `GET /tasks`: Listar tarefas
- `GET /tasks/{id}`: Obter tarefa por ID
- `PUT /tasks/{id}`: Atualizar tarefa
- `DELETE /tasks/{id}`: Excluir tarefa

## Testes

Execute os testes: `pytest`