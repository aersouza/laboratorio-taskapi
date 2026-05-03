from __future__ import annotations

from typing import Optional

from app.models.task import Priority


class PriorityAdvisor:
    """Componente responsável por sugerir a prioridade de uma tarefa."""

    def analyze_task(self, title: str, description: Optional[str] = None) -> Priority:
        """Analisa título e descrição para sugerir uma prioridade inicial."""
        normalized_text = " ".join(filter(None, [title, description or ""])).lower()

        if any(keyword in normalized_text for keyword in ["urgente", "agora", "imediato", "crítico", "crítica", "bloqueio"]):
            return Priority.CRITICA

        if any(keyword in normalized_text for keyword in ["atraso", "importante", "prioridade alta", "alta"]):
            return Priority.ALTA

        if any(keyword in normalized_text for keyword in ["melhoria", "refator", "refatoração", "documentação", "ajuste"]):
            return Priority.MEDIA

        return Priority.BAIXA
