"""
Módulo de modelos SQLAlchemy para tarefas.

Este módulo define a classe Task que representa uma tarefa no banco de dados.
"""

from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from app.database import Base


class TaskStatus(str, Enum):
    """Enumeração dos status possíveis para uma tarefa."""
    PENDENTE = "pendente"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDA = "concluida"


class Task(Base):
    """
    Modelo SQLAlchemy para representar uma tarefa no banco de dados.
    
    Atributos:
        id (int): Identificador único da tarefa.
        title (str): Título da tarefa (indexado para buscas rápidas).
        description (str): Descrição detalhada da tarefa (opcional).
        status (TaskStatus): Status atual da tarefa (pendente, em_progresso, concluida).
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDENTE, nullable=False)