# Escopo do MVP — laboratorio-taskapi

## 1. Objetivo do Projeto

O objetivo do MVP `laboratorio-taskapi` é fornecer uma micro-API de gerenciamento de tarefas para uso interno da equipe. A API deve ser uma solução leve e confiável para criação, consulta, atualização e remoção de tarefas, com suporte a status de execução e filtragem, permitindo integração com sistemas internos e automações.

O MVP deve garantir:
- entrega rápida com arquitetura modular;
- uso de tecnologias padrão em Python para desenvolvimento web e persistência de dados;
- API RESTful simples, testável e com documentação básica.

## 2. Requisitos Funcionais

### 2.1 Operações CRUD de Tarefas
- `POST /tasks`
  - criar nova tarefa com campos: título, descrição e status.
  - título obrigatório, mínimo 1 e máximo 100 caracteres.
  - descrição opcional, máximo 500 caracteres.
  - status padrão: `pendente`.
  - resposta: objeto da tarefa criada com `id` e `status`.

- `GET /tasks`
  - listar tarefas existentes.
  - suportar paginação por `skip` e `limit`.
  - permitir filtro por `status` (`pendente`, `em_progresso`, `concluida`).
  - resposta: lista de tarefas em JSON.

- `GET /tasks/{id}`
  - obter os dados de tarefa pelo identificador.
  - validação de existência; retorna 404 se não existir.
  - resposta: dados completos da tarefa.

- `PUT /tasks/{id}`
  - atualizar título, descrição e status de tarefa existente.
  - validação de entrada equivalente ao endpoint de criação.
  - resposta: tarefa atualizada.

- `PATCH /tasks/{id}/complete`
  - marcar tarefa como concluída.
  - altera somente o status para `concluida`.
  - validação de existência; retorna 404 se não existir.
  - resposta: tarefa com status atualizado.

- `DELETE /tasks/{id}`
  - remover tarefa existente.
  - validação de existência; retorna 404 se não existir.
  - resposta: confirmação de exclusão.

### 2.2 Healthcheck e Monitoramento Básico
- `GET /health`
  - retorna status de serviço `ok` e `timestamp` atual do sistema.
  - utiliza modelo Pydantic para validar o payload de resposta.

## 3. Requisitos Não Funcionais

### 3.1 Arquitetura e Organização do Código
- organização modular em pacotes separados:
  - `app/models` para entidades SQLAlchemy;
  - `app/schemas` para validação Pydantic;
  - `app/routes` para definições de endpoints;
  - `app/services` para lógica de negócio;
  - `app/database.py` para configuração de persistência.
- o ponto de entrada deve ser `app/main.py`.
- código com tipagem estática `typing` e docstrings explicativas.

### 3.2 Persistência de Dados
- banco de dados SQLite local para MVP.
- uso de SQLAlchemy como ORM.
- configuração de `requirements.txt` para dependências.

### 3.3 Qualidade de Software
- testes unitários obrigatórios para:
  - serviços de negócio;
  - controladores/endpoints.
- cobertura de testes mínima esperada: 90% no código da aplicação.
- uso de `pytest` e `pytest-cov` para validação.

### 3.4 Documentação e Uso
- README atualizado com:
  - objetivo do projeto;
  - instruções de instalação e execução;
  - descrição de endpoints;
  - instruções para testes.
- documentação interativa via FastAPI em `/docs`.

### 3.5 Manutenibilidade
- código escrito com práticas de Clean Code.
- separação entre camada de roteamento e camada de negócio.
- uso de modelos Pydantic para padronização de payloads.

## 4. Fora de Escopo

- autenticação e autorização de usuários;
- controle de acesso por perfis ou roles;
- funcionalidades de usuários, equipes ou projetos;
- interface web ou UI frontend;
- integração com serviços externos de notificação ou chat;
- sistema de tags ou categorias avançadas para tarefas;
- controle de anexos, upload de arquivos ou mídia;
- escalabilidade horizontal, cache distribuído ou fila de mensagens;
- deploy automatizado em ambiente de produção;
- métricas avançadas de performance, observabilidade ou tracing.

## 5. Entregáveis do MVP

- API RESTful funcional com endpoints CRUD e healthcheck;
- backend em Python com FastAPI e SQLAlchemy;
- banco SQLite local configurado;
- testes unitários para serviços e endpoints;
- README completo e atualizado;
- esquema de pastas modular e documentado;
- modelo Pydantic para validação de dados e resposta do healthcheck.

## 6. Critérios de Aceitação

- endpoints funcionam conforme especificado;
- resultados validados por testes automatizados;
- API documentada em `/docs` e README;
- código modular, legível e com tipagem explícita;
- healthcheck funcional retornando `status: ok` e timestamp UTC.
