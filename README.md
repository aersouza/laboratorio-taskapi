# Laboratorio TaskAPI

Micro-API de tarefas construída com FastAPI, organizada em camadas e com sugestão de prioridade assistida por IA com fallback local.

O MVP implementa operações CRUD para tarefas, sugestão automática de prioridade e testes automatizados para serviço, advisor e rotas.

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

## Instalação

Clone o repositório e acesse o diretório do projeto:

```bash
git clone https://github.com/aersouza/laboratorio-taskapi.git
cd laboratorio-taskapi
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
```

Windows:

```bash
.\venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Execute a aplicação com Uvicorn:

```bash
uvicorn app.main:app --reload
```

A documentação interativa fica disponível em:

```text
http://127.0.0.1:8000/docs
```

Healthcheck:

```bash
curl http://127.0.0.1:8000/health
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

### Listar Tarefas

```http
GET /tasks/?status=pendente&skip=0&limit=100
```

Status esperado:

```text
200 OK
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

1. Chamada externa opcional via biblioteca `openai`, quando `OPENAI_API_KEY` estiver configurada.
2. Heurística local como comportamento padrão ou fallback.

Variáveis de ambiente suportadas:

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `OPENAI_API_KEY` | vazio | Habilita chamada externa quando presente. |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Modelo usado na chamada externa. |
| `PRIORITY_ADVISOR_TIMEOUT` | `3` | Timeout da chamada externa em segundos. |

Heurística local:

| Prioridade | Palavras-chave |
| --- | --- |
| `crítica` | `urgente`, `agora`, `imediato`, `crítico`, `crítica`, `bloqueio` |
| `alta` | `atraso`, `importante`, `alta prioridade`, `alta` |
| `média` | `melhoria`, `refator`, `refatoração`, `documentação`, `ajuste`, `revisão` |
| `baixa` | Padrão quando nenhuma regra anterior é acionada. |

## Testes

Execute todas as suítes atuais:

```bash
pytest tests/test_task_service.py tests/test_priority_advisor.py tests/test_task_routes.py
```

Execute com cobertura:

```bash
pytest tests/test_task_service.py tests/test_priority_advisor.py tests/test_task_routes.py --cov=app
```

Suítes disponíveis:

| Arquivo | Cobertura |
| --- | --- |
| `tests/test_task_service.py` | CRUD do `TaskService` e casos de ID inexistente. |
| `tests/test_priority_advisor.py` | Heurística local, parse de prioridade e fallback. |
| `tests/test_task_routes.py` | Status HTTP `201`, `200`, `204` e `404` com `TestClient`. |

## Limitações

- O repositório atual é em memória; os dados são perdidos ao reiniciar a aplicação.
- Não há autenticação ou autorização.
- Não há controle de concorrência para o repositório em memória.
- A integração externa do `PriorityAdvisor` depende da biblioteca `openai` estar instalada e configurada.
- O modelo externo configurado por padrão é legado e deve ser revisado antes de uso produtivo.
- Os warnings de depreciação atuais indicam pontos futuros de manutenção em `datetime.utcnow()` e dependências FastAPI/Starlette/httpx.

## Próximos Passos

- Atualizar `PriorityAdvisor` para o cliente moderno da OpenAI.
- Trocar `datetime.utcnow()` por datetimes timezone-aware.
- Adicionar autenticação com JWT ou API key.
- Adicionar logs estruturados e middleware de correlação.
- Criar configuração por ambiente com `.env`.
- Adicionar pipeline de CI para testes e cobertura.
