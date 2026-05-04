# Laboratorio TaskAPI

Micro-API de tarefas construída com FastAPI, organizada em camadas e com sugestão de prioridade assistida por IA com fallback local.

O MVP implementa operações CRUD para tarefas, sugestão automática de prioridade e testes automatizados para serviço, advisor e rotas.

Esta versão não utiliza banco de dados, ORM ou migrações. A persistência ativa do MVP é em memória, via `TaskRepository`.

## Sumário

- [Stack](#stack)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Execução](#execução)
- [Endpoints](#endpoints)
- [Prioridade Assistida](#prioridade-assistida)
- [Testes](#testes)
- [Limitações](#limitações)
- [Próximos Passos](#próximos-passos)

## Stack

- Python
- FastAPI
- Pydantic
- Pytest
- Uvicorn

Versão recomendada:

- Python 3.11+

Fora do escopo atual:

- SQLAlchemy
- Alembic
- SQLite ou outro banco persistente

## Funcionalidades

- Criar tarefa.
- Listar tarefas com paginação e filtro por status.
- Buscar tarefa por ID.
- Atualizar tarefa.
- Excluir tarefa.
- Retornar `404` para IDs inexistentes.
- Sugerir prioridade com `PriorityAdvisor`.
- Executar fallback local quando a chamada externa estiver indisponível.

## Arquitetura

```text
laboratorio-taskapi/
├── app/
│   ├── api/
│   │   └── task_routes.py
│   ├── models/
│   │   └── task.py
│   ├── repositories/
│   │   └── task_repository.py
│   ├── services/
│   │   ├── priority_advisor.py
│   │   └── task_service.py
│   └── main.py
├── tests/
│   ├── test_priority_advisor.py
│   ├── test_task_routes.py
│   └── test_task_service.py
├── docs/
│   └── diagramas.md
├── .env.example
├── Makefile
├── requirements.txt
└── README.md
```

### Camadas

| Camada | Arquivo | Responsabilidade |
| --- | --- | --- |
| API | `app/api/task_routes.py` | Endpoints HTTP, status codes e tratamento de `404`. |
| Service | `app/services/task_service.py` | Orquestra regras de negócio e integra repositório com advisor. |
| Advisor | `app/services/priority_advisor.py` | Sugere prioridade por LLM opcional ou heurística local. |
| Repository | `app/repositories/task_repository.py` | Persistência em memória e operações CRUD. |
| Models | `app/models/task.py` | Enums e schemas Pydantic usados pela implementação atual. |

Diagramas complementares estão disponíveis em `docs/diagramas.md`.

> Não há camada de banco nesta versão. `TaskRepository` usa um `dict[int, TaskOut]` em memória e os dados são descartados quando o processo reinicia.

## Instalação

Clone o repositório e acesse o diretório do projeto:

```bash
git clone https://github.com/aersouza/laboratorio-taskapi.git
cd laboratorio-taskapi
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

Windows:

```bash
.\.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Ou use o Makefile:

```bash
make install
```

O `requirements.txt` contém apenas dependências necessárias para a API, testes e execução local. Não há dependências de banco de dados ou migração.

Prepare as variáveis de ambiente opcionais:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

> O arquivo `.env` não é carregado automaticamente pela aplicação. Para habilitar a chamada externa do `PriorityAdvisor`, exporte as variáveis no ambiente antes de executar a API.

## Execução

Execute a aplicação com Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

Ou use o Makefile:

```bash
make run
```

É possível customizar host e porta:

```bash
make run HOST=0.0.0.0 PORT=8080
```

A documentação interativa fica disponível em:

```text
http://127.0.0.1:8000/docs
```

Healthcheck:

```bash
curl http://127.0.0.1:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "timestamp": "2026-05-03T20:26:01.699917-03:00"
}
```

## Endpoints

### Criar Tarefa

```http
POST /tasks/
```

Body:

```json
{
  "title": "Corrigir bug crítico",
  "description": "Erro bloqueia o fluxo principal",
  "status": "pendente"
}
```

Status esperado:

```text
201 Created
```

Exemplo com `curl`:

```bash
curl -X POST http://127.0.0.1:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Corrigir bloqueio urgente","description":"Fluxo principal parado agora","status":"pendente"}'
```

### Listar Tarefas

```http
GET /tasks/?status=pendente&skip=0&limit=100
```

Status esperado:

```text
200 OK
```

Exemplo com `curl`:

```bash
curl "http://127.0.0.1:8000/tasks/?status=pendente&skip=0&limit=100"
```

### Buscar Tarefa por ID

```http
GET /tasks/{task_id}
```

Status esperados:

```text
200 OK
404 Not Found
```

### Atualizar Tarefa

```http
PUT /tasks/{task_id}
```

Body:

```json
{
  "title": "Corrigir bug crítico atualizado",
  "description": "Fluxo principal impactado",
  "status": "em_progresso",
  "priority": "alta"
}
```

Status esperados:

```text
200 OK
404 Not Found
```

### Excluir Tarefa

```http
DELETE /tasks/{task_id}
```

Status esperados:

```text
204 No Content
404 Not Found
```

## Modelo de Dados

### Status

| Valor | Descrição |
| --- | --- |
| `pendente` | Tarefa aguardando execução. |
| `em_progresso` | Tarefa em andamento. |
| `concluida` | Tarefa concluída. |

### Prioridade

| Valor | Descrição |
| --- | --- |
| `baixa` | Baixa prioridade. |
| `média` | Prioridade intermediária. |
| `alta` | Alta prioridade. |
| `crítica` | Prioridade crítica. |

### Exemplo de Resposta

```json
{
  "id": 1,
  "title": "Corrigir bug crítico",
  "description": "Erro bloqueia o fluxo principal",
  "status": "pendente",
  "priority": null,
  "priority_suggestion": "crítica",
  "created_at": "2026-05-03T19:00:00.000000",
  "updated_at": "2026-05-03T19:00:00.000000"
}
```

## Prioridade Assistida

O `PriorityAdvisor` sugere prioridade com duas estratégias:

1. Heurística local como comportamento padrão.
2. Chamada externa opcional via biblioteca `openai`, quando `OPENAI_API_KEY` estiver configurada e a dependência opcional estiver instalada.

Por padrão, a API funciona sem LLM externo. Se `OPENAI_API_KEY` não estiver definida, se a biblioteca `openai` não estiver instalada, se ocorrer erro ou timeout, o advisor usa a heurística local.

Variáveis de ambiente suportadas:

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `OPENAI_API_KEY` | vazio | Habilita chamada externa quando presente. |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Modelo usado na chamada externa. |
| `PRIORITY_ADVISOR_TIMEOUT` | `3` | Timeout da chamada externa em segundos. |

Exemplo de `.env`:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo
PRIORITY_ADVISOR_TIMEOUT=3
```

Para usar a chamada externa com a implementação atual, instale a dependência opcional compatível:

```bash
python -m pip install openai==0.28.1
```

> A implementação atual usa a API legada `ChatCompletion.create`. Antes de uso produtivo, recomenda-se atualizar o `PriorityAdvisor` para o SDK moderno da OpenAI.

Heurística local:

| Prioridade | Palavras-chave |
| --- | --- |
| `crítica` | `urgente`, `agora`, `imediato`, `crítico`, `crítica`, `bloqueio` |
| `alta` | `atraso`, `importante`, `alta prioridade`, `alta` |
| `média` | `melhoria`, `refator`, `refatoração`, `documentação`, `ajuste`, `revisão` |
| `baixa` | Padrão quando nenhuma regra anterior é acionada. |

Exemplos de entrada:

| Payload | `priority_suggestion` |
| --- | --- |
| `{"title": "Corrigir bloqueio urgente"}` | `crítica` |
| `{"title": "Resolver atraso importante"}` | `alta` |
| `{"title": "Melhoria na documentação"}` | `média` |
| `{"title": "Organizar backlog"}` | `baixa` |

O campo `priority_suggestion` é informativo. O campo `priority`, quando enviado em atualização, representa a prioridade definida pelo cliente.

## Testes

Execute todas as suítes atuais:

```bash
python -m pytest tests/test_task_service.py tests/test_priority_advisor.py tests/test_task_routes.py
```

Ou use o Makefile:

```bash
make test
```

Execute com cobertura:

```bash
python -m pytest tests/test_task_service.py tests/test_priority_advisor.py tests/test_task_routes.py --cov=app
```

Suítes disponíveis:

| Arquivo | Cobertura |
| --- | --- |
| `tests/test_task_service.py` | CRUD do `TaskService` e casos de ID inexistente. |
| `tests/test_priority_advisor.py` | Heurística local, parse de prioridade e fallback. |
| `tests/test_task_routes.py` | Status HTTP `201`, `200`, `204`, `404`, validações `422` e sugestões `alta`/`média` com `TestClient`. |

## Limitações

- O repositório atual é em memória; os dados são perdidos ao reiniciar a aplicação.
- Não há autenticação ou autorização.
- Não há controle de concorrência para o repositório em memória.
- A integração externa do `PriorityAdvisor` depende da biblioteca opcional `openai` estar instalada e configurada.
- O `.env` não é carregado automaticamente; as variáveis devem existir no ambiente do processo.
- O cliente OpenAI usado no código atual é legado e deve ser revisado antes de uso produtivo.
- Os warnings de depreciação atuais indicam pontos futuros de manutenção em `datetime.utcnow()` e dependências FastAPI/Starlette/httpx.

## Próximos Passos

- Atualizar `PriorityAdvisor` para o cliente moderno da OpenAI.
- Trocar `datetime.utcnow()` por datetimes timezone-aware.
- Adicionar autenticação com JWT ou API key.
- Adicionar logs estruturados e middleware de correlação.
- Carregar configuração por ambiente automaticamente a partir de `.env`.
- Adicionar pipeline de CI para testes e cobertura.
