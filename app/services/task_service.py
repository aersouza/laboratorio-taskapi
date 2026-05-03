"""Serviço de tarefas que separa regra de negócio da camada de API."""

from typing import List, Optional

from app.models.task import Priority, TaskCreate, TaskOut, TaskStatus, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor


class TaskService:
    """Camada de serviço para operações de tarefas."""

    def __init__(self, repository: TaskRepository, advisor: PriorityAdvisor) -> None:
        self._repository = repository
        self._advisor = advisor

    def create_task(self, payload: TaskCreate) -> TaskOut:
        """Cria uma tarefa com sugestão de prioridade."""
        priority_suggestion = self._suggest_priority(
            title=payload.title,
            description=payload.description,
        )
        return self._repository.create(
            payload,
            priority_suggestion=priority_suggestion,
        )

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[TaskOut]:
        """Retorna tarefas com filtro de status e paginação."""
        return self._repository.list(status=status, skip=skip, limit=limit)

    def get_task_by_id(self, task_id: int) -> Optional[TaskOut]:
        """Busca uma tarefa pelo ID."""
        return self._repository.get_by_id(task_id)

    def update_task(self, task_id: int, payload: TaskUpdate) -> Optional[TaskOut]:
        """Atualiza tarefa e recalcula sugestão de prioridade quando necessário."""
        existing = self._repository.get_by_id(task_id)
        if existing is None:
            return None

        priority_suggestion = None
        if payload.title is not None or payload.description is not None:
            title, description = self._merge_task_text(existing, payload)
            priority_suggestion = self._suggest_priority(
                title=title,
                description=description,
            )

        return self._repository.update(
            task_id,
            payload,
            priority_suggestion=priority_suggestion,
        )

    def delete_task(self, task_id: int) -> bool:
        """Remove uma tarefa do repositório."""
        try:
            self._repository.delete(task_id)
            return True
        except KeyError:
            return False

    def mark_task_as_completed(self, task_id: int) -> Optional[TaskOut]:
        """Marca tarefa como concluída."""
        payload = TaskUpdate(status=TaskStatus.CONCLUIDA)
        try:
            return self._repository.update(task_id, payload)
        except KeyError:
            return None

    def _suggest_priority(
        self,
        title: str,
        description: Optional[str] = None,
    ) -> Priority:
        return self._advisor.analyze_task(
            title=title,
            description=description,
        )

    def _merge_task_text(
        self,
        existing: TaskOut,
        payload: TaskUpdate,
    ) -> tuple[str, Optional[str]]:
        title = payload.title if payload.title is not None else existing.title
        description = (
            payload.description
            if payload.description is not None
            else existing.description
        )
        return title, description
