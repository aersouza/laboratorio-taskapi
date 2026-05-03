import pytest

from app.models.task import Priority, TaskCreate, TaskStatus, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


class FakePriorityAdvisor:
    def __init__(self, priority: Priority = Priority.MEDIA) -> None:
        self.priority = priority
        self.calls: list[tuple[str, str | None]] = []

    def analyze_task(self, title: str, description: str | None = None) -> Priority:
        self.calls.append((title, description))
        return self.priority


@pytest.fixture
def advisor() -> FakePriorityAdvisor:
    return FakePriorityAdvisor(priority=Priority.ALTA)


@pytest.fixture
def service(advisor: FakePriorityAdvisor) -> TaskService:
    return TaskService(repository=TaskRepository(), advisor=advisor)


def test_create_task_returns_created_task_with_priority_suggestion(
    service: TaskService,
    advisor: FakePriorityAdvisor,
) -> None:
    payload = TaskCreate(
        title="Corrigir bug crítico",
        description="Erro bloqueia o fluxo principal",
        status=TaskStatus.PENDENTE,
    )

    task = service.create_task(payload)

    assert task.id == 1
    assert task.title == payload.title
    assert task.description == payload.description
    assert task.status == TaskStatus.PENDENTE
    assert task.priority is None
    assert task.priority_suggestion == Priority.ALTA
    assert advisor.calls == [(payload.title, payload.description)]


def test_list_tasks_returns_all_tasks_in_creation_order(service: TaskService) -> None:
    first = service.create_task(TaskCreate(title="Primeira tarefa"))
    second = service.create_task(TaskCreate(title="Segunda tarefa"))

    tasks = service.list_tasks()

    assert tasks == [first, second]


def test_list_tasks_filters_by_status(service: TaskService) -> None:
    pending = service.create_task(
        TaskCreate(title="Tarefa pendente", status=TaskStatus.PENDENTE)
    )
    service.create_task(
        TaskCreate(title="Tarefa concluída", status=TaskStatus.CONCLUIDA)
    )

    tasks = service.list_tasks(status=TaskStatus.PENDENTE)

    assert tasks == [pending]


def test_update_task_changes_fields_and_recalculates_priority_suggestion(
    service: TaskService,
    advisor: FakePriorityAdvisor,
) -> None:
    created = service.create_task(
        TaskCreate(title="Título inicial", description="Descrição inicial")
    )
    advisor.calls.clear()

    updated = service.update_task(
        created.id,
        TaskUpdate(title="Título atualizado", status=TaskStatus.EM_PROGRESSO),
    )

    assert updated is not None
    assert updated.id == created.id
    assert updated.title == "Título atualizado"
    assert updated.description == "Descrição inicial"
    assert updated.status == TaskStatus.EM_PROGRESSO
    assert updated.priority_suggestion == Priority.ALTA
    assert advisor.calls == [("Título atualizado", "Descrição inicial")]


def test_delete_task_removes_task(service: TaskService) -> None:
    created = service.create_task(TaskCreate(title="Tarefa para excluir"))

    deleted = service.delete_task(created.id)

    assert deleted is True
    assert service.get_task_by_id(created.id) is None


def test_get_task_by_id_returns_none_for_missing_id(service: TaskService) -> None:
    task = service.get_task_by_id(999)

    assert task is None


def test_update_task_returns_none_for_missing_id(service: TaskService) -> None:
    updated = service.update_task(999, TaskUpdate(title="Não existe"))

    assert updated is None


def test_delete_task_returns_false_for_missing_id(service: TaskService) -> None:
    deleted = service.delete_task(999)

    assert deleted is False
