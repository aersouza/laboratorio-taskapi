"""
Testes para a camada de serviços de tarefas.

Este módulo contém testes unitários para validar a lógica de negócio
da camada de serviços usando pytest e SQLAlchemy.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService

# Configuração do banco de testes
TEST_DATABASE_URL = "sqlite:///./test_services.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    """Fixture que fornece uma sessão de banco limpa para cada teste."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


class TestTaskServiceCreate:
    """Testes para criação de tarefas no serviço."""

    def test_create_task_with_all_fields(self, db):
        """Testa criação de tarefa com todos os campos."""
        task_create = TaskCreate(
            title="Nova tarefa",
            description="Descrição completa",
            status=TaskStatus.EM_PROGRESSO
        )
        
        task = TaskService.create_task(db, task_create)
        
        assert task.id is not None
        assert task.title == "Nova tarefa"
        assert task.description == "Descrição completa"
        assert task.status == TaskStatus.EM_PROGRESSO

    def test_create_task_with_minimal_fields(self, db):
        """Testa criação de tarefa com apenas título."""
        task_create = TaskCreate(title="Tarefa simples")
        
        task = TaskService.create_task(db, task_create)
        
        assert task.title == "Tarefa simples"
        assert task.status == TaskStatus.PENDENTE
        assert task.description is None

    def test_create_task_persists_in_db(self, db):
        """Testa se a tarefa criada é persistida no banco."""
        task_create = TaskCreate(title="Tarefa persistente")
        task = TaskService.create_task(db, task_create)
        task_id = task.id
        
        # Recuperar a tarefa do banco
        retrieved_task = db.query(Task).filter(Task.id == task_id).first()
        
        assert retrieved_task is not None
        assert retrieved_task.title == "Tarefa persistente"


class TestTaskServiceRead:
    """Testes para leitura de tarefas no serviço."""

    def test_get_tasks_empty(self, db):
        """Testa listagem com nenhuma tarefa."""
        tasks = TaskService.get_tasks(db)
        assert tasks == []

    def test_get_tasks_with_data(self, db):
        """Testa listagem com múltiplas tarefas."""
        for i in range(3):
            TaskService.create_task(db, TaskCreate(title=f"Tarefa {i}"))
        
        tasks = TaskService.get_tasks(db)
        assert len(tasks) == 3

    def test_get_tasks_with_skip_and_limit(self, db):
        """Testa listagem com paginação."""
        for i in range(5):
            TaskService.create_task(db, TaskCreate(title=f"Tarefa {i}"))
        
        tasks = TaskService.get_tasks(db, skip=1, limit=2)
        assert len(tasks) == 2

    def test_get_tasks_filter_by_status(self, db):
        """Testa filtro por status."""
        TaskService.create_task(db, TaskCreate(title="Pendente", status=TaskStatus.PENDENTE))
        TaskService.create_task(db, TaskCreate(title="Em Progresso", status=TaskStatus.EM_PROGRESSO))
        TaskService.create_task(db, TaskCreate(title="Outra Pendente", status=TaskStatus.PENDENTE))
        
        pending_tasks = TaskService.get_tasks(db, status=TaskStatus.PENDENTE)
        assert len(pending_tasks) == 2

    def test_get_task_by_id_success(self, db):
        """Testa recuperação de tarefa por ID."""
        created_task = TaskService.create_task(db, TaskCreate(title="Tarefa teste"))
        
        retrieved_task = TaskService.get_task_by_id(db, created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.title == "Tarefa teste"

    def test_get_task_by_id_not_found(self, db):
        """Testa recuperação de tarefa inexistente."""
        task = TaskService.get_task_by_id(db, 999)
        assert task is None


class TestTaskServiceUpdate:
    """Testes para atualização de tarefas no serviço."""

    def test_update_task_success(self, db):
        """Testa atualização bem-sucedida de uma tarefa."""
        created_task = TaskService.create_task(db, TaskCreate(title="Original"))
        
        task_update = TaskUpdate(
            title="Atualizada",
            description="Nova descrição",
            status=TaskStatus.EM_PROGRESSO
        )
        
        updated_task = TaskService.update_task(db, created_task.id, task_update)
        
        assert updated_task.title == "Atualizada"
        assert updated_task.description == "Nova descrição"
        assert updated_task.status == TaskStatus.EM_PROGRESSO

    def test_update_task_not_found(self, db):
        """Testa atualização de tarefa inexistente."""
        task_update = TaskUpdate(title="Não vai atualizar")
        updated_task = TaskService.update_task(db, 999, task_update)
        
        assert updated_task is None

    def test_update_task_partial(self, db):
        """Testa atualização parcial de tarefa."""
        created_task = TaskService.create_task(
            db,
            TaskCreate(title="Original", description="Descrição original")
        )
        
        task_update = TaskUpdate(title="Novo título")
        updated_task = TaskService.update_task(db, created_task.id, task_update)
        
        assert updated_task.title == "Novo título"


class TestTaskServiceDelete:
    """Testes para exclusão de tarefas no serviço."""

    def test_delete_task_success(self, db):
        """Testa exclusão bem-sucedida de uma tarefa."""
        created_task = TaskService.create_task(db, TaskCreate(title="A deletar"))
        
        success = TaskService.delete_task(db, created_task.id)
        
        assert success is True
        
        # Verificar que foi deletada
        deleted_task = TaskService.get_task_by_id(db, created_task.id)
        assert deleted_task is None

    def test_delete_task_not_found(self, db):
        """Testa exclusão de tarefa inexistente."""
        success = TaskService.delete_task(db, 999)
        assert success is False


class TestTaskServiceCompleteTask:
    """Testes para marcar tarefa como concluída."""

    def test_mark_task_as_completed_success(self, db):
        """Testa marcação bem-sucedida de tarefa como concluída."""
        created_task = TaskService.create_task(
            db,
            TaskCreate(title="A completar", status=TaskStatus.PENDENTE)
        )
        
        completed_task = TaskService.mark_task_as_completed(db, created_task.id)
        
        assert completed_task is not None
        assert completed_task.status == TaskStatus.CONCLUIDA

    def test_mark_task_as_completed_not_found(self, db):
        """Testa marcação de tarefa inexistente como concluída."""
        completed_task = TaskService.mark_task_as_completed(db, 999)
        assert completed_task is None

    def test_mark_already_completed_task(self, db):
        """Testa marcação de tarefa já concluída."""
        created_task = TaskService.create_task(
            db,
            TaskCreate(title="Já concluída", status=TaskStatus.CONCLUIDA)
        )
        
        completed_task = TaskService.mark_task_as_completed(db, created_task.id)
        
        assert completed_task.status == TaskStatus.CONCLUIDA