# Backlog do MVP — laboratorio-taskapi

Este backlog define as tarefas mínimas para entrega do MVP em 3 releases: Core, Qualidade e Entrega Final. Cada item possui ID único (RF para Requisito Funcional, RT para Requisito Técnico) e critérios de aceite claros.

## Release 1: Core (Funcionalidades Básicas)

### RF-001: Implementar endpoint POST /tasks
- [ ] Criar endpoint para criação de tarefas
- [ ] Validar entrada com Pydantic (título obrigatório, descrição opcional)
- [ ] Persistir no banco SQLite via SQLAlchemy
- [ ] Retornar tarefa criada com ID gerado
- **Critérios de Aceite:**
  - Requisição POST com JSON válido retorna 201 e tarefa criada
  - Validação rejeita títulos vazios ou >100 caracteres
  - Descrição opcional aceita até 500 caracteres

### RF-002: Implementar endpoint GET /tasks
- [ ] Criar endpoint para listagem de tarefas
- [ ] Suportar paginação (skip, limit)
- [ ] Filtrar por status (pendente, em_progresso, concluida)
- [ ] Retornar lista de tarefas em JSON
- **Critérios de Aceite:**
  - GET sem parâmetros retorna todas as tarefas
  - Parâmetros skip/limit funcionam corretamente
  - Filtro por status retorna apenas tarefas correspondentes

### RF-003: Implementar endpoint GET /tasks/{id}
- [ ] Criar endpoint para obter tarefa específica
- [ ] Validar existência do ID
- [ ] Retornar 404 se tarefa não existir
- [ ] Retornar dados completos da tarefa
- **Critérios de Aceite:**
  - ID válido retorna tarefa em JSON
  - ID inexistente retorna 404 com mensagem clara

### RF-004: Implementar endpoint PUT /tasks/{id}
- [ ] Criar endpoint para atualização completa de tarefa
- [ ] Validar entrada e existência do ID
- [ ] Atualizar título, descrição e status
- [ ] Retornar tarefa atualizada
- **Critérios de Aceite:**
  - Atualização bem-sucedida retorna tarefa modificada
  - Validação rejeita entradas inválidas
  - ID inexistente retorna 404

### RF-005: Implementar endpoint PATCH /tasks/{id}/complete
- [ ] Criar endpoint para marcar tarefa como concluída
- [ ] Alterar apenas status para "concluida"
- [ ] Validar existência do ID
- [ ] Retornar tarefa com status atualizado
- **Critérios de Aceite:**
  - PATCH bem-sucedido altera status para "concluida"
  - ID inexistente retorna 404

### RF-006: Implementar endpoint DELETE /tasks/{id}
- [ ] Criar endpoint para exclusão de tarefa
- [ ] Validar existência do ID
- [ ] Remover tarefa do banco
- [ ] Retornar confirmação de exclusão
- **Critérios de Aceite:**
  - DELETE bem-sucedido remove tarefa e retorna 204
  - ID inexistente retorna 404

### RF-007: Implementar endpoint GET /health
- [ ] Criar endpoint de healthcheck
- [ ] Retornar status "ok" e timestamp UTC
- [ ] Usar modelo Pydantic para resposta
- **Critérios de Aceite:**
  - GET retorna JSON com status e timestamp válido
  - Timestamp em formato ISO 8601 UTC

### RT-001: Configurar estrutura modular da aplicação
- [ ] Criar pacotes app/models, app/schemas, app/routes, app/services
- [ ] Configurar database.py com SQLAlchemy e SQLite
- [ ] Definir main.py como ponto de entrada
- **Critérios de Aceite:**
  - Estrutura de pastas criada conforme especificado
  - Imports funcionam corretamente entre módulos

### RT-002: Implementar modelos SQLAlchemy
- [ ] Criar modelo Task com campos id, title, description, status
- [ ] Definir enum TaskStatus com valores válidos
- [ ] Configurar Base e engine
- **Critérios de Aceite:**
  - Modelo cria tabela corretamente no SQLite
  - Campos com tipos e restrições adequadas

### RT-003: Implementar esquemas Pydantic
- [ ] Criar TaskBase, TaskCreate, TaskUpdate, Task
- [ ] Definir validações de campo (min/max length)
- [ ] Configurar from_attributes para SQLAlchemy
- **Critérios de Aceite:**
  - Validações rejeitam entradas inválidas
  - Serialização/deserialização funciona com modelos SQLAlchemy

## Release 2: Qualidade (Testes e Documentação)

### RT-004: Implementar testes unitários para serviços
- [ ] Criar test_services.py com 17 testes
- [ ] Testar CRUD completo no TaskService
- [ ] Testar filtros e paginação
- [ ] Usar fixtures para banco de testes
- **Critérios de Aceite:**
  - Todos os testes passam
  - Cobertura >90% nos serviços

### RT-005: Implementar testes unitários para endpoints
- [ ] Criar test_tasks.py com 16 testes
- [ ] Testar todos os endpoints CRUD
- [ ] Testar validações e erros 404
- [ ] Usar TestClient do FastAPI
- **Critérios de Aceite:**
  - Todos os testes passam
  - Cobertura >90% nos endpoints

### RT-006: Configurar pytest-cov para cobertura
- [ ] Instalar pytest-cov
- [ ] Configurar comando para relatório de cobertura
- [ ] Verificar cobertura total >90%
- **Critérios de Aceite:**
  - Comando pytest --cov funciona
  - Relatório mostra cobertura detalhada

### RT-007: Adicionar docstrings completas
- [ ] Documentar todos os módulos, classes e funções
- [ ] Usar formato Google/NumPy para docstrings
- [ ] Incluir tipos em type hints
- **Critérios de Aceite:**
  - Todas as funções/classes têm docstrings
  - Type hints estão presentes

### RT-008: Atualizar README com documentação completa
- [ ] Descrever objetivo, instalação e execução
- [ ] Listar todos os endpoints com exemplos
- [ ] Incluir instruções de testes
- **Critérios de Aceite:**
  - README cobre todos os aspectos do projeto
  - Exemplos funcionam conforme descrito

## Release 3: Entrega Final (Preparação para Produção)

### RT-009: Criar documento de escopo do MVP
- [ ] Documentar objetivo, requisitos funcionais/não funcionais
- [ ] Definir fora de escopo
- [ ] Incluir critérios de aceitação
- **Critérios de Aceite:**
  - Documento completo em docs/escopo-mvp.md
  - Aprovado pela equipe

### RT-010: Criar backlog do projeto
- [ ] Listar tarefas por release
- [ ] Atribuir IDs RF/RT únicos
- [ ] Definir critérios de aceite para cada item
- **Critérios de Aceite:**
  - Backlog em docs/backlog.md
  - Todos os itens têm IDs e critérios

### RT-011: Configurar .gitignore adequado
- [ ] Ignorar __pycache__, *.pyc, *.db
- [ ] Incluir .env, venv/, etc.
- [ ] Verificar arquivos não rastreados
- **Critérios de Aceite:**
  - git status limpo após configuração
  - Arquivos sensíveis não commitados

### RT-012: Preparar requirements.txt final
- [ ] Listar todas as dependências com versões
- [ ] Incluir FastAPI, SQLAlchemy, pytest, etc.
- [ ] Testar instalação limpa
- **Critérios de Aceite:**
  - pip install -r requirements.txt funciona
  - Ambiente virtual instala corretamente

### RT-013: Validar documentação FastAPI
- [ ] Verificar /docs e /redoc funcionam
- [ ] Testar exemplos interativos
- [ ] Confirmar schemas Pydantic aparecem
- **Critérios de Aceite:**
  - Documentação acessível e completa
  - Exemplos executáveis funcionam

### RT-014: Executar testes finais e cobertura
- [ ] Rodar pytest completo
- [ ] Verificar cobertura >90%
- [ ] Corrigir qualquer falha
- **Critérios de Aceite:**
  - Todos os testes passam
  - Cobertura mínima atingida