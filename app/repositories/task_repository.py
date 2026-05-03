"""Repositório em memória para persistência inicial de tarefas."""

from datetime import datetime
from typing import Optional

from app.models.task import Priority, TaskCreate, TaskOut, TaskUpdate, TaskStatus


class TaskRepository:
    """Repositório em memória para gerenciar tarefas."""

    def __init__(self) -> None:
        self._storage: dict[int, TaskOut] = {}
        self._next_id: int = 1

    def create(
        self,
        payload: TaskCreate,
        priority_suggestion: Optional[Priority] = None,
    ) -> TaskOut:
        """Cria uma nova tarefa em memória."""
        task = self._build_task(payload, priority_suggestion)
        self._storage[task.id] = task
        self._next_id += 1
        return task

    def list(
        self,
        *,
        status: Optional[TaskStatus] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TaskOut]:
        """Retorna tarefas armazenadas, com filtro opcional e paginação."""
        tasks = [
            task
            for task in self._storage.values()
            if status is None or task.status == status
        ]
        return tasks[skip : skip + limit]

    def get_by_id(self, task_id: int) -> Optional[TaskOut]:
        """Retorna uma tarefa pelo identificador ou None se não existir."""
        return self._storage.get(task_id)

    def update(
        self,
        task_id: int,
        payload: TaskUpdate,
        priority_suggestion: Optional[Priority] = None,
    ) -> TaskOut:
        """Atualiza uma tarefa existente em memória."""
        existing = self.get_by_id(task_id)
        if existing is None:
            self._raise_not_found(task_id)

        update_data = self._build_update_data(payload, priority_suggestion)
        updated_task = existing.model_copy(update=update_data)
        updated_task = updated_task.model_copy(update={"updated_at": self._now()})
        self._storage[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> None:
        """Remove uma tarefa do repositório em memória."""
        if task_id not in self._storage:
            self._raise_not_found(task_id)
        del self._storage[task_id]

    def _build_task(
        self,
        payload: TaskCreate,
        priority_suggestion: Optional[Priority],
    ) -> TaskOut:
        now = self._now()
        return TaskOut(
            id=self._next_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=None,
            priority_suggestion=priority_suggestion,
            created_at=now,
            updated_at=now,
        )

    def _build_update_data(
        self,
        payload: TaskUpdate,
        priority_suggestion: Optional[Priority],
    ) -> dict:
        update_data = payload.model_dump(exclude_none=True)
        if priority_suggestion is not None:
            update_data["priority_suggestion"] = priority_suggestion
        return update_data

    def _now(self) -> datetime:
        return datetime.utcnow()

    def _raise_not_found(self, task_id: int) -> None:
        raise KeyError(f"Task {task_id} not found")
