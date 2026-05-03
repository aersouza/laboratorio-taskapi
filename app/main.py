"""
Módulo principal da aplicação FastAPI.

Este módulo define a instância FastAPI e implementa o endpoint
de healthcheck para verificar o estado da API.
"""

from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

from app.api.task_routes import router as task_router


class HealthCheckResponse(BaseModel):
    """Modelo de resposta para o endpoint de healthcheck."""

    status: str
    timestamp: str


app = FastAPI(
    title="Laboratorio TaskAPI",
    description="Micro-API de To-Do List com healthcheck e status de serviço",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(task_router)


@app.get("/health", response_model=HealthCheckResponse, tags=["health"])
def health_check() -> HealthCheckResponse:
    """
    Endpoint de healthcheck da API.

    Retorna o status atual do serviço e o timestamp do sistema no momento da requisição.

    Returns:
        HealthCheckResponse: Estado do serviço e carimbo de data/hora em UTC.
    """
    return HealthCheckResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat()
    )
