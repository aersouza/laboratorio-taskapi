"""PriorityAdvisor com heurística local e fallback opcional para LLM.

A chamada remota ocorre somente quando OPENAI_API_KEY estiver configurada
no ambiente. O comportamento padrão é local, com timeout explícito e
fallback seguro para garantir operação sem custo.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import Optional

from app.models.task import Priority

logger = logging.getLogger(__name__)

_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
_OPENAI_TIMEOUT = int(os.getenv("PRIORITY_ADVISOR_TIMEOUT", "3"))


class PriorityAdvisor:
    """Componente responsável por sugerir prioridade de tarefas."""

    def __init__(self, model: str = _OPENAI_MODEL, timeout_seconds: int = _OPENAI_TIMEOUT) -> None:
        self._model = model
        self._timeout_seconds = timeout_seconds
        self._openai = self._load_openai_client()
        self._enabled = self._openai is not None and bool(_OPENAI_API_KEY)

    def _load_openai_client(self):
        if not _OPENAI_API_KEY:
            logger.debug("OPENAI_API_KEY não encontrado; usando apenas heurística local.")
            return None

        try:
            openai = importlib.import_module("openai")
            openai.api_key = _OPENAI_API_KEY
            return openai
        except ImportError:
            logger.warning("Biblioteca openai não instalada; fallback para heurística local.")
            return None
        except Exception as exc:
            logger.warning("Erro ao inicializar cliente OpenAI; fallback para heurística local.", exc_info=exc)
            return None

    def analyze_task(self, title: str, description: Optional[str] = None) -> Priority:
        """Retorna prioridade sugerida usando LLM opcional ou heurística local."""
        if self._enabled:
            try:
                return self._query_llm(title=title, description=description)
            except Exception as exc:
                logger.warning("LLM indisponível ou timeout; usando heurística local.", exc_info=exc)

        return self._local_heuristic(title=title, description=description)

    def _query_llm(self, title: str, description: Optional[str] = None) -> Priority:
        assert self._openai is not None

        prompt = self._build_prompt(title=title, description=description)
        payload = {
            "model": self._model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente que sugere um nível de prioridade "
                        "para uma tarefa de software. Retorne apenas uma das opções: "
                        "baixa, média, alta, crítica."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.0,
        }

        try:
            response = self._openai.ChatCompletion.create(
                **payload,
                timeout=self._timeout_seconds,
            )
        except TypeError:
            response = self._openai.ChatCompletion.create(
                **payload,
                request_timeout=self._timeout_seconds,
            )

        text = self._extract_response_text(response)
        return self._parse_priority(text)

    def _extract_response_text(self, response) -> str:
        choice = response.choices[0]
        message = getattr(choice, "message", None) or choice["message"]
        content = message.content if hasattr(message, "content") else message["content"]
        return str(content).strip()

    def _build_prompt(self, title: str, description: Optional[str] = None) -> str:
        details = title.strip()
        if description:
            details = f"{details}. Descrição: {description.strip()}"
        return f"Analise a tarefa e sugira prioridade: {details}"

    def _parse_priority(self, raw: str) -> Priority:
        lower = raw.lower()
        if "crít" in lower or "crit" in lower:
            return Priority.CRITICA
        if "alta" in lower:
            return Priority.ALTA
        if "méd" in lower or "med" in lower:
            return Priority.MEDIA
        return Priority.BAIXA

    def _local_heuristic(self, title: str, description: Optional[str] = None) -> Priority:
        normalized = " ".join(filter(None, [title, description or ""]))
        normalized = normalized.lower()

        if any(keyword in normalized for keyword in ["urgente", "agora", "imediato", "crítico", "crítica", "bloqueio"]):
            return Priority.CRITICA

        if any(keyword in normalized for keyword in ["atraso", "importante", "alta prioridade", "alta"]):
            return Priority.ALTA

        if any(keyword in normalized for keyword in ["melhoria", "refator", "refatoração", "documentação", "ajuste", "revisão"]):
            return Priority.MEDIA

        return Priority.BAIXA
