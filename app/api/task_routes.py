"""Rotas HTTP para gerenciamento de tarefas."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.models.task import TaskCreate, TaskOut, TaskStatus, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

_repository = TaskRepository()
_priority_advisor = PriorityAdvisor()
_task_service = TaskService(repository=_repository, advisor=_priority_advisor)


def get_task_service() -> TaskService:
    """Retorna a instância compartilhada do serviço de tarefas."""
    return _task_service


TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]


@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreate,
    service: TaskServiceDependency,
) -> TaskOut:
    return service.create_task(payload)


@router.get("/", response_model=list[TaskOut])
def list_tasks(
    service: TaskServiceDependency,
    status_filter: Annotated[TaskStatus | None, Query(alias="status")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[TaskOut]:
    return service.list_tasks(
        status=status_filter,
        skip=skip,
        limit=limit,
    )


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    service: TaskServiceDependency,
) -> TaskOut:
    task = service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskServiceDependency,
) -> TaskOut:
    task = service.update_task(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_task(
    task_id: int,
    service: TaskServiceDependency,
) -> Response:
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
