"""
Módulo de esquemas Pydantic para validação de tarefas.

Este módulo define os esquemas Pydantic para entrada e saída de dados
nas operações de tarefas, garantindo validação e serialização corretas.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """Enumeração dos status possíveis para uma tarefa."""
    PENDENTE = "pendente"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDA = "concluida"


class TaskBase(BaseModel):
    """Classe base com campos comuns a todos os esquemas de tarefas."""
    title: str = Field(..., min_length=1, max_length=100, description="Título da tarefa")
    description: Optional[str] = Field(None, max_length=500, description="Descrição da tarefa")
    status: TaskStatus = Field(TaskStatus.PENDENTE, description="Status da tarefa")


class TaskCreate(TaskBase):
    """Esquema para criação de uma nova tarefa."""
    pass


class TaskUpdate(TaskBase):
    """Esquema para atualização de uma tarefa existente."""
    pass


class Task(TaskBase):
    """
    Esquema para representação completa de uma tarefa.
    
    Inclui o ID gerado pelo banco de dados e configuração
    para converter objetos SQLAlchemy em dicionários.
    """
    id: int = Field(..., description="Identificador único da tarefa")

    model_config = ConfigDict(from_attributes=True)