"""
Módulo de serviços para operações de tarefas.

Este módulo contém a lógica de negócio para CRUD de tarefas,
separada dos endpoints para melhor testabilidade e reutilização.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Serviço que encapsula a lógica de negócio para tarefas."""

    @staticmethod
    def create_task(db: Session, task: TaskCreate) -> Task:
        """
        Cria uma nova tarefa no banco de dados.
        
        Args:
            db (Session): Sessão do banco de dados.
            task (TaskCreate): Dados da tarefa a ser criada.
        
        Returns:
            Task: Tarefa criada com ID gerado.
        """
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        status: Optional[TaskStatus] = None
    ) -> List[Task]:
        """
        Lista tarefas com filtros opcionais.
        
        Args:
            db (Session): Sessão do banco de dados.
            skip (int): Número de registros a pular (padrão: 0).
            limit (int): Número máximo de registros a retornar (padrão: 10).
            status (Optional[TaskStatus]): Filtrar por status (opcional).
        
        Returns:
            List[Task]: Lista de tarefas encontradas.
        """
        query = db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
        """
        Obtém uma tarefa pelo ID.
        
        Args:
            db (Session): Sessão do banco de dados.
            task_id (int): ID da tarefa a ser recuperada.
        
        Returns:
            Optional[Task]: Tarefa encontrada ou None.
        """
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """
        Atualiza uma tarefa existente.
        
        Args:
            db (Session): Sessão do banco de dados.
            task_id (int): ID da tarefa a ser atualizada.
            task_update (TaskUpdate): Novos dados da tarefa.
        
        Returns:
            Optional[Task]: Tarefa atualizada ou None se não encontrada.
        """
        db_task = TaskService.get_task_by_id(db, task_id)
        if not db_task:
            return None
        
        for key, value in task_update.model_dump().items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        """
        Deleta uma tarefa pelo ID.
        
        Args:
            db (Session): Sessão do banco de dados.
            task_id (int): ID da tarefa a ser deletada.
        
        Returns:
            bool: True se a tarefa foi deletada, False se não encontrada.
        """
        db_task = TaskService.get_task_by_id(db, task_id)
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True

    @staticmethod
    def mark_task_as_completed(db: Session, task_id: int) -> Optional[Task]:
        """
        Marca uma tarefa como concluída.
        
        Args:
            db (Session): Sessão do banco de dados.
            task_id (int): ID da tarefa a ser marcada como concluída.
        
        Returns:
            Optional[Task]: Tarefa atualizada ou None se não encontrada.
        """
        db_task = TaskService.get_task_by_id(db, task_id)
        if not db_task:
            return None
        
        db_task.status = TaskStatus.CONCLUIDA
        db.commit()
        db.refresh(db_task)
        return db_task