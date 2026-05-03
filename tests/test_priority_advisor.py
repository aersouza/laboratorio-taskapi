import pytest

from app.models.task import Priority
from app.services.priority_advisor import PriorityAdvisor


@pytest.fixture
def advisor() -> PriorityAdvisor:
    return PriorityAdvisor()


@pytest.mark.parametrize(
    ("title", "description", "expected_priority"),
    [
        ("Corrigir bloqueio urgente", None, Priority.CRITICA),
        ("Resolver atraso importante", None, Priority.ALTA),
        ("Melhoria na documentação", "Revisão do guia de uso", Priority.MEDIA),
        ("Organizar backlog", None, Priority.BAIXA),
    ],
)
def test_analyze_task_uses_local_heuristic_priority_levels(
    advisor: PriorityAdvisor,
    monkeypatch: pytest.MonkeyPatch,
    title: str,
    description: str | None,
    expected_priority: Priority,
) -> None:
    monkeypatch.setattr(advisor, "_enabled", False)

    priority = advisor.analyze_task(title=title, description=description)

    assert priority == expected_priority


def test_analyze_task_falls_back_to_local_heuristic_when_llm_fails(
    advisor: PriorityAdvisor,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_query_llm(title: str, description: str | None = None) -> Priority:
        raise TimeoutError("LLM timeout")

    monkeypatch.setattr(advisor, "_enabled", True)
    monkeypatch.setattr(advisor, "_query_llm", fail_query_llm)

    priority = advisor.analyze_task(
        title="Corrigir bloqueio urgente",
        description="Fluxo principal parado agora",
    )

    assert priority == Priority.CRITICA


@pytest.mark.parametrize(
    ("raw_response", "expected_priority"),
    [
        ("prioridade crítica", Priority.CRITICA),
        ("alta", Priority.ALTA),
        ("média", Priority.MEDIA),
        ("sem urgência", Priority.BAIXA),
    ],
)
def test_parse_priority_maps_llm_response_to_supported_priority(
    advisor: PriorityAdvisor,
    raw_response: str,
    expected_priority: Priority,
) -> None:
    priority = advisor._parse_priority(raw_response)

    assert priority == expected_priority
