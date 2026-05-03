import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.task_routes import get_task_service, router
from app.models.task import Priority
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


class FakePriorityAdvisor:
    def analyze_task(self, title: str, description: str | None = None) -> Priority:
        return Priority.ALTA


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


def test_create_task_returns_201(client: TestClient) -> None:
    response = client.post(
        "/tasks/",
        json={
            "title": "Implementar testes de rota",
            "description": "Cobrir endpoints CRUD",
            "status": "pendente",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Implementar testes de rota",
        "description": "Cobrir endpoints CRUD",
        "status": "pendente",
        "priority": None,
        "priority_suggestion": "alta",
        "created_at": response.json()["created_at"],
        "updated_at": response.json()["updated_at"],
    }


def test_list_tasks_returns_200(client: TestClient) -> None:
    client.post("/tasks/", json={"title": "Primeira tarefa"})
    client.post("/tasks/", json={"title": "Segunda tarefa"})

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == [
        "Primeira tarefa",
        "Segunda tarefa",
    ]


def test_get_task_by_id_returns_200(client: TestClient) -> None:
    created = client.post("/tasks/", json={"title": "Buscar por ID"}).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["title"] == "Buscar por ID"


def test_update_task_returns_200(client: TestClient) -> None:
    created = client.post("/tasks/", json={"title": "Título antigo"}).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={
            "title": "Título atualizado",
            "description": "Descrição atualizada",
            "status": "em_progresso",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["title"] == "Título atualizado"
    assert response.json()["description"] == "Descrição atualizada"
    assert response.json()["status"] == "em_progresso"


def test_delete_task_returns_204(client: TestClient) -> None:
    created = client.post("/tasks/", json={"title": "Excluir tarefa"}).json()

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_get_missing_task_returns_404(client: TestClient) -> None:
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_missing_task_returns_404(client: TestClient) -> None:
    response = client.put("/tasks/999", json={"title": "Não existe"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_missing_task_returns_404(client: TestClient) -> None:
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
