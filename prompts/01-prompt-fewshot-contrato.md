# Prompt 1: Few-Shot / Estrutural (Contrato de API e Caminho Feliz)

## Papel
Você é um engenheiro de testes sênior especialista em testes de integração de APIs REST em Python usando `pytest` e `httpx` (ou `TestClient`).

## Tarefa
Crie um arquivo de teste de integração para o endpoint `POST /tasks` (ou `/api/tasks`) da aplicação `taskapi`.

## Requisito
Gere os testes em Python cobrindo a criação e listagem de tarefas válidas (Status HTTP 200/201), retornando apenas o código executável.

## Exemplo de Estrutura Esperada (Few-Shot)
```python
import pytest

def test_deve_criar_tarefa_com_sucesso(client):
    payload = {
        "title": "Ajustar pipeline de CI/CD",
        "description": "Configurar automação dos testes",
        "status": "pending"
    }
    response = client.post("/tasks", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == payload["title"]