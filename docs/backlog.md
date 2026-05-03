# Backlog do MVP — laboratorio-taskapi

Este backlog define as tarefas mínimas para entrega do MVP seguindo **desenvolvimento ágil** com releases incrementais e frequentes. Cada item possui ID único (RF para Requisito Funcional, RT para Requisito Técnico) e critérios de aceite claros. Cada release agrega valor real e é independentemente deployável.

---

## Release 1: MVP Mínimo (Criar e Listar)

**Objetivo:** Disponibilizar funcionalidade básica de criação e listagem de tarefas.  
**Duração estimada:** 1 sprint (1-2 semanas)  
**Valor entregue:** Usuários podem criar tarefas e visualizar lista completa.

### RF-001: Implementar endpoint POST /tasks
- [ ] Criar endpoint para criação de tarefas com título obrigatório
- [ ] Validar entrada com Pydantic (título 1-100 caracteres, descrição opcional até 500)
- [ ] Persistir no banco SQLite via SQLAlchemy
- [ ] Retornar tarefa criada com ID e status padrão "pendente"
- **Critérios de Aceite:**
  - Requisição POST com JSON válido retorna 201 e tarefa criada
  - Validação rejeita títulos vazios ou >100 caracteres
  - Resposta inclui id, title, description, status

### RF-002: Implementar endpoint GET /tasks (listagem simples)
- [ ] Criar endpoint para listar todas as tarefas
- [ ] Retornar lista completa em JSON
- [ ] Sem paginação ou filtros nesta release
- **Critérios de Aceite:**
  - GET /tasks retorna array de tarefas
  - Lista vazia retorna array vazio []

### RT-001: Configurar estrutura modular da aplicação
- [ ] Criar pacotes app/models, app/schemas, app/routes, app/services
- [ ] Configurar database.py com SQLAlchemy e SQLite
- [ ] Definir main.py como ponto de entrada
- **Critérios de Aceite:**
  - Estrutura de pastas criada conforme especificado
  - Imports funcionam corretamente entre módulos

### RT-002: Implementar modelos e esquemas Pydantic
- [ ] Criar modelo Task com campos id, title, description, status
- [ ] Definir enum TaskStatus com valores (pendente, em_progresso, concluida)
- [ ] Criar esquemas Pydantic: TaskBase, TaskCreate, Task
- [ ] Configurar Base e engine SQLAlchemy
- **Critérios de Aceite:**
  - Modelo cria tabela corretamente no SQLite
  - Esquemas validam entrada e serializam saída

### RT-003: Testes unitários para Release 1
- [ ] Criar test_tasks.py com testes para POST e GET /tasks
- [ ] Testar criação com dados válidos e inválidos
- [ ] Testar listagem vazia e com dados
- [ ] Usar TestClient do FastAPI e fixtures
- **Critérios de Aceite:**
  - Testes passam com cobertura >85% para endpoints
  - Validações são testadas (título vazio, muito longo, etc)

---

## Release 2: CRUD Completo, Filtros e Paginação

**Objetivo:** Completar funcionalidades CRUD com filtros, paginação e operações completas.  
**Duração estimada:** 2 sprints (2-4 semanas)  
**Valor entregue:** Usuários podem gerenciar ciclo completo e navegar grandes listas.

### RF-003: Implementar endpoint GET /tasks/{id}
- [ ] Criar endpoint para obter tarefa específica por ID
- [ ] Validar existência do ID
- [ ] Retornar 404 se tarefa não existir
- [ ] Retornar dados completos da tarefa
- **Critérios de Aceite:**
  - ID válido retorna tarefa em JSON
  - ID inexistente retorna 404 com mensagem clara

### RF-004: Implementar endpoint PUT /tasks/{id}
- [ ] Criar endpoint para atualizar título, descrição e status
- [ ] Validar entrada e existência do ID
- [ ] Retornar 404 se tarefa não existir
- [ ] Retornar tarefa atualizada
- **Critérios de Aceite:**
  - PUT bem-sucedido atualiza tarefa completa
  - Validações rejeitam entradas inválidas
  - ID inexistente retorna 404

### RF-005: Implementar endpoint DELETE /tasks/{id}
- [ ] Criar endpoint para exclusão de tarefa
- [ ] Validar existência do ID
- [ ] Remover tarefa do banco
- [ ] Retornar 204 ou 404
- **Critérios de Aceite:**
  - DELETE bem-sucedido remove tarefa e retorna 204
  - ID inexistente retorna 404

### RF-006: Implementar endpoint PATCH /tasks/{id}/complete
- [ ] Criar endpoint para marcar tarefa como concluída
- [ ] Alterar apenas status para "concluida"
- [ ] Validar existência do ID
- [ ] Retornar tarefa com status atualizado
- **Critérios de Aceite:**
  - PATCH bem-sucedido altera status para "concluida"
  - ID inexistente retorna 404

### RF-007: Expandir GET /tasks com paginação
- [ ] Adicionar parâmetros skip e limit
- [ ] Testar paginação com múltiplos registros
- [ ] Retornar total de itens na resposta
- **Critérios de Aceite:**
  - skip/limit funcionam corretamente
  - Resposta inclui count total de itens

### RF-008: Filtrar tarefas por status
- [ ] Adicionar parâmetro status ao GET /tasks
- [ ] Suportar valores: pendente, em_progresso, concluida
- [ ] Funciona em conjunto com paginação
- **Critérios de Aceite:**
  - Filtro por status retorna apenas tarefas correspondentes
  - Combinação com paginação funciona

### RT-004: Testes unitários para Release 2
- [ ] Testar PUT, DELETE, PATCH, GET /{id}
- [ ] Testar filtros e paginação
- [ ] Testar cenários de erro (ID não encontrado)
- [ ] Expandir cobertura para >85%
- **Critérios de Aceite:**
  - Testes cobrem todas as operações CRUD
  - Filtros e paginação testados
  - Cobertura >85% nos endpoints

---

## Release 3: Monitoramento, Qualidade e Entrega

**Objetivo:** Maturar projeto com healthcheck, documentação completa, testes robustos e preparação para manutenção contínua.  
**Duração estimada:** 2-3 sprints (2-6 semanas)  
**Valor entregue:** Projeto pronto para produção com monitoramento, documentação e testes confiáveis.

### RF-009: Implementar endpoint GET /health
- [ ] Criar endpoint de healthcheck
- [ ] Retornar status "ok" e timestamp UTC em ISO 8601
- [ ] Usar modelo Pydantic para resposta
- **Critérios de Aceite:**
  - GET /health retorna {status: "ok", timestamp: "2026-05-03T..."}
  - Timestamp está em UTC

### RT-005: Testes unitários para serviços
- [ ] Criar test_services.py com testes para lógica de negócio
- [ ] Testar CRUD completo no TaskService
- [ ] Testar filtros e paginação
- [ ] Usar fixtures para banco de testes
- **Critérios de Aceite:**
  - Todos os testes de serviços passam
  - Cobertura >90% nos serviços

### RT-006: Adicionar docstrings e type hints completos
- [ ] Documentar todos os módulos, classes e funções
- [ ] Usar formato Google para docstrings
- [ ] Verificar type hints em todas as funções
- **Critérios de Aceite:**
  - 100% das funções/classes têm docstrings
  - Type hints cobrem parâmetros e retornos

### RT-007: Configurar pytest-cov e validar cobertura total
- [ ] Instalar pytest-cov
- [ ] Executar testes com relatório de cobertura
- [ ] Verificar cobertura total >90%
- **Critérios de Aceite:**
  - Comando pytest --cov funciona
  - Relatório mostra cobertura detalhada
  - Todos os testes passam

### RT-008: Atualizar README com documentação completa
- [ ] Descrever objetivo, instalação, execução
- [ ] Listar todos os endpoints com exemplos de curl
- [ ] Incluir instruções para rodar testes
- [ ] Documentar estrutura de pastas
- **Critérios de Aceite:**
  - README cobre instalação, uso e testes
  - Exemplos são copiáveis e funcionam

### RT-009: Validar documentação FastAPI interativa
- [ ] Verificar /docs (Swagger) está acessível
- [ ] Testar /redoc (ReDoc)
- [ ] Confirmar que todos os endpoints aparecem
- **Critérios de Aceite:**
  - Documentação interativa funciona em /docs
  - Schemas Pydantic aparecem corretamente

### RT-010: Preparar project para produção
- [ ] Verificar .gitignore (ignorar __pycache__, *.db, venv/)
- [ ] Preparar requirements.txt com todas as dependências versionadas
- [ ] Documentar versão do projeto e changelog
- **Critérios de Aceite:**
  - git status limpo, sem arquivos sensíveis
  - pip install -r requirements.txt funciona
  - requirements.txt especifica versões mínimas

---

## Diferenças da Abordagem Ágil

| Aspecto | Waterfall (anterior) | Ágil (novo) |
|--------|---------------------|-----------|
| **Releases** | 3 releases (Core, Qualidade, Deploy) | 3 releases incrementais com valor|
| **Testes** | Concentrados em fase específica | Distribuídos em cada release |
| **Deploy** | Apenas no final | A cada release (1-2 meses) |
| **Feedback** | Após tudo pronto | Após cada release |
| **Valor** | Entregue no final | Incrementalmente |
| **Riscos** | Altos no começo | Distribuídos |

### Cronograma Estimado

- **Release 1:** MVP Mínimo → 1-2 semanas
- **Release 2:** CRUD Completo + Filtros → 2-4 semanas
- **Release 3:** Qualidade + Documentação → 2-6 semanas
- **Total estimado:** 5-12 semanas (1-3 meses)

### Benefícios desta Abordagem

✅ **Feedback antecipado:** Usuários podem testar após Release 1  
✅ **Mitigação de riscos:** Problemas detectados mais cedo  
✅ **Entregas rápidas:** Valor ao usuário a cada 1-2 meses  
✅ **Flexibilidade:** Ajustes conforme feedback real  
✅ **Motivação da equipe:** Vitórias incrementais