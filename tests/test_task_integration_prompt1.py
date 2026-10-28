import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.task_routes import get_task_service, router
from app.models.task import Priority
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


class FakePriorityAdvisor:
    def analyze_task(
        self,
        title: str,
        description: str | None = None,
    ) -> Priority:
        return Priority.BAIXA


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    service = TaskService(
        repository=TaskRepository(),
        advisor=FakePriorityAdvisor(),
    )

    app.dependency_overrides[get_task_service] = lambda: service
    app.include_router(router)
    return TestClient(app)


def test_deve_criar_tarefa_com_sucesso(client: TestClient) -> None:
    payload = {
        "title": "Ajustar pipeline de CI/CD",
        "description": "Configurar automação dos testes",
        "status": "pendente",
    }

    response = client.post("/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == payload["status"]


def test_deve_listar_tarefas_com_sucesso(client: TestClient) -> None:
    client.post("/tasks/", json={"title": "Primeira tarefa"})
    client.post("/tasks/", json={"title": "Segunda tarefa"})

    response = client.get("/tasks/")

    assert response.status_code == 200
    data = response.json()
    assert [task["title"] for task in data] == [
        "Primeira tarefa",
        "Segunda tarefa",
    ]
