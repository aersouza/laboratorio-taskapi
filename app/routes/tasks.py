"""
Módulo de rotas para operações de tarefas.

Este módulo define os endpoints RESTful para CRUD de tarefas,
delegando a lógica de negócio para a camada de serviços.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskStatus
from app.services.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    """
    Cria uma nova tarefa.
    
    Args:
        task (TaskCreate): Dados da tarefa a ser criada.
        db (Session): Sessão do banco de dados.
    
    Returns:
        Task: Tarefa criada com ID gerado.
    
    Raises:
        HTTPException: Erro 400 se os dados forem inválidos.
    """
    return TaskService.create_task(db, task)


@router.get("/", response_model=List[Task])
def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[TaskStatus] = Query(None),
    db: Session = Depends(get_db)
) -> List[Task]:
    """
    Lista tarefas com filtros opcionais.
    
    Args:
        skip (int): Número de registros a pular (padrão: 0).
        limit (int): Número máximo de registros a retornar (padrão: 10, máximo: 100).
        status (Optional[TaskStatus]): Filtrar por status (pendente, em_progresso, concluida).
        db (Session): Sessão do banco de dados.
    
    Returns:
        List[Task]: Lista de tarefas.
    """
    return TaskService.get_tasks(db, skip=skip, limit=limit, status=status)


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    """
    Obtém uma tarefa específica pelo ID.
    
    Args:
        task_id (int): ID da tarefa a ser recuperada.
        db (Session): Sessão do banco de dados.
    
    Returns:
        Task: Detalhes da tarefa.
    
    Raises:
        HTTPException: Erro 404 se a tarefa não for encontrada.
    """
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
) -> Task:
    """
    Atualiza uma tarefa existente.
    
    Args:
        task_id (int): ID da tarefa a ser atualizada.
        task_update (TaskUpdate): Novos dados da tarefa.
        db (Session): Sessão do banco de dados.
    
    Returns:
        Task: Tarefa atualizada.
    
    Raises:
        HTTPException: Erro 404 se a tarefa não for encontrada.
    """
    task = TaskService.update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}/complete", response_model=Task)
def complete_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    """
    Marca uma tarefa como concluída.
    
    Args:
        task_id (int): ID da tarefa a ser marcada como concluída.
        db (Session): Sessão do banco de dados.
    
    Returns:
        Task: Tarefa com status atualizado para "concluida".
    
    Raises:
        HTTPException: Erro 404 se a tarefa não for encontrada.
    """
    task = TaskService.mark_task_as_completed(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """
    Deleta uma tarefa pelo ID.
    
    Args:
        task_id (int): ID da tarefa a ser deletada.
        db (Session): Sessão do banco de dados.
    
    Raises:
        HTTPException: Erro 404 se a tarefa não for encontrada.
    """
    success = TaskService.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")