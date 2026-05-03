"""
Testes para os endpoints da API de tarefas.

Este módulo contém testes unitários para validar os endpoints
CRUD da API usando pytest e TestClient.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

# Configuração do banco de testes
TEST_DATABASE_URL = "sqlite:///./test_tasks.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Sobrescreve a dependência get_db para usar o banco de testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    """Limpa o banco de dados antes de cada teste."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


class TestCreateTask:
    """Testes para criação de tarefas."""

    def test_create_task_success(self):
        """Testa criação bem-sucedida de uma tarefa."""
        response = client.post(
            "/tasks/",
            json={
                "title": "Minha primeira tarefa",
                "description": "Descrição da tarefa",
                "status": "pendente"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minha primeira tarefa"
        assert data["status"] == "pendente"
        assert "id" in data

    def test_create_task_minimal(self):
        """Testa criação de tarefa com apenas título."""
        response = client.post(
            "/tasks/",
            json={"title": "Tarefa simples"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Tarefa simples"
        assert data["status"] == "pendente"
        assert data["description"] is None

    def test_create_task_invalid_title(self):
        """Testa criação com título vazio (inválido)."""
        response = client.post(
            "/tasks/",
            json={"title": ""}
        )
        assert response.status_code == 422

    def test_create_task_title_too_long(self):
        """Testa criação com título excedendo 100 caracteres."""
        response = client.post(
            "/tasks/",
            json={"title": "x" * 101}
        )
        assert response.status_code == 422


class TestReadTasks:
    """Testes para listagem de tarefas."""

    def test_read_empty_tasks(self):
        """Testa listagem com nenhuma tarefa."""
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_read_tasks_with_data(self):
        """Testa listagem com múltiplas tarefas."""
        # Criar 3 tarefas
        for i in range(3):
            client.post("/tasks/", json={"title": f"Tarefa {i}"})
        
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_read_tasks_with_pagination(self):
        """Testa listagem com skip e limit."""
        for i in range(5):
            client.post("/tasks/", json={"title": f"Tarefa {i}"})
        
        response = client.get("/tasks/?skip=1&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_read_tasks_filter_by_status(self):
        """Testa filtro por status."""
        client.post("/tasks/", json={"title": "Pendente 1", "status": "pendente"})
        client.post("/tasks/", json={"title": "Em Progresso", "status": "em_progresso"})
        client.post("/tasks/", json={"title": "Pendente 2", "status": "pendente"})
        
        response = client.get("/tasks/?status=pendente")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestReadTaskById:
    """Testes para leitura de tarefa específica."""

    def test_read_task_success(self):
        """Testa leitura bem-sucedida de uma tarefa."""
        create_response = client.post(
            "/tasks/",
            json={"title": "Tarefa para ler"}
        )
        task_id = create_response.json()["id"]
        
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Tarefa para ler"

    def test_read_task_not_found(self):
        """Testa leitura de tarefa inexistente."""
        response = client.get("/tasks/999")
        assert response.status_code == 404


class TestUpdateTask:
    """Testes para atualização de tarefas."""

    def test_update_task_success(self):
        """Testa atualização bem-sucedida de uma tarefa."""
        create_response = client.post(
            "/tasks/",
            json={"title": "Tarefa original"}
        )
        task_id = create_response.json()["id"]
        
        response = client.put(
            f"/tasks/{task_id}",
            json={
                "title": "Tarefa atualizada",
                "description": "Nova descrição",
                "status": "em_progresso"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Tarefa atualizada"
        assert data["status"] == "em_progresso"

    def test_update_task_not_found(self):
        """Testa atualização de tarefa inexistente."""
        response = client.put(
            "/tasks/999",
            json={"title": "Nova tarefa"}
        )
        assert response.status_code == 404


class TestCompleteTask:
    """Testes para marcar tarefa como concluída."""

    def test_complete_task_success(self):
        """Testa marcação bem-sucedida como concluída."""
        create_response = client.post(
            "/tasks/",
            json={"title": "Tarefa a completar"}
        )
        task_id = create_response.json()["id"]
        
        response = client.patch(f"/tasks/{task_id}/complete")
        assert response.status_code == 200
        assert response.json()["status"] == "concluida"

    def test_complete_task_not_found(self):
        """Testa marcação de tarefa inexistente como concluída."""
        response = client.patch("/tasks/999/complete")
        assert response.status_code == 404


class TestDeleteTask:
    """Testes para exclusão de tarefas."""

    def test_delete_task_success(self):
        """Testa exclusão bem-sucedida de uma tarefa."""
        create_response = client.post(
            "/tasks/",
            json={"title": "Tarefa a deletar"}
        )
        task_id = create_response.json()["id"]
        
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204
        
        # Verificar que foi deletada
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self):
        """Testa exclusão de tarefa inexistente."""
        response = client.delete("/tasks/999")
        assert response.status_code == 404