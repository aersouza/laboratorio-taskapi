"""
Módulo principal da aplicação FastAPI.

Este módulo define a instância FastAPI e implementa o endpoint
de healthcheck para verificar o estado da API.
"""

from datetime import datetime, timezone
from fastapi import FastAPI


app = FastAPI(
    title="Laboratorio TaskAPI",
    description="Micro-API de To-Do List com healthcheck e status de serviço",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """
    Endpoint de healthcheck da API.

    Retorna o status atual do serviço e o timestamp do sistema no momento da requisição.

    Returns:
        dict[str, str]: Dicionário com chaves 'status' e 'timestamp'.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }