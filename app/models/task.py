"""Enums e schemas Pydantic para tarefas."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Estados possíveis de uma tarefa."""

    PENDENTE = "pendente"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDA = "concluida"


class Priority(str, Enum):
    """Níveis de prioridade suportados."""

    BAIXA = "baixa"
    MEDIA = "média"
    ALTA = "alta"
    CRITICA = "crítica"


class TaskCreate(BaseModel):
    """
    Schema para criação de uma nova tarefa.

    Atributos:
        title: Título da tarefa (1-100 caracteres, obrigatório).
        description: Descrição opcional (máx 500 caracteres).
        status: Status inicial (padrão: pendente).
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Implementar PriorityAdvisor"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        examples=["Componente para sugerir prioridades automaticamente"],
    )
    status: TaskStatus = Field(default=TaskStatus.PENDENTE)


class TaskUpdate(BaseModel):
    """
    Schema para atualização de uma tarefa.

    Todos os campos são opcionais. Apenas campos fornecidos serão atualizados.

    Atributos:
        title: Novo título (opcional).
        description: Nova descrição (opcional).
        status: Novo status (opcional).
        priority: Nova prioridade (opcional).
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
    )
    status: Optional[TaskStatus] = Field(default=None)
    priority: Optional[Priority] = Field(default=None)


class TaskOut(BaseModel):
    """
    Schema para resposta/leitura de uma tarefa.

    Inclui sugestão de prioridade do PriorityAdvisor.

    Atributos:
        id: Identificador único.
        title: Título da tarefa.
        description: Descrição da tarefa.
        status: Status atual.
        priority: Prioridade da tarefa.
        priority_suggestion: Sugestão do PriorityAdvisor.
        created_at: Timestamp de criação.
        updated_at: Timestamp de última atualização.
    """

    model_config = {"from_attributes": True}

    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Optional[Priority] = None
    priority_suggestion: Optional[Priority] = Field(default=None)
    created_at: datetime
    updated_at: datetime
