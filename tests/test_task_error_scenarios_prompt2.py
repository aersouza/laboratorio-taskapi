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


def test_deve_rejeitar_titulo_em_branco(client: TestClient) -> None:
    response = client.post(
        "/tasks/",
        json={"title": "", "description": "Descrição válida"},
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "title"] for error in errors)


def test_deve_rejeitar_titulo_ausente(client: TestClient) -> None:
    response = client.post(
        "/tasks/",
        json={"description": "Tarefa sem título"},
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(
        error["loc"] == ["body", "title"] and error["type"] == "missing"
        for error in errors
    )


def test_deve_rejeitar_status_invalido(client: TestClient) -> None:
    response = client.post(
        "/tasks/",
        json={"title": "Tarefa", "status": "status_inexistente"},
    )

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "status"] for error in errors)


def test_deve_retornar_404_ao_buscar_tarefa_inexistente(
    client: TestClient,
) -> None:
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_deve_retornar_404_ao_atualizar_tarefa_inexistente(
    client: TestClient,
) -> None:
    response = client.put(
        "/tasks/999999",
        json={"title": "Atualização"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_deve_retornar_404_ao_deletar_tarefa_inexistente(
    client: TestClient,
) -> None:
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_deve_rejeitar_id_com_formato_invalido(client: TestClient) -> None:
    response = client.get("/tasks/id-invalido")

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["loc"] == ["path", "task_id"] for error in errors)
