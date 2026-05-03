"""
Módulo principal da aplicação FastAPI.

Este módulo configura e inicializa a aplicação FastAPI,
incluindo criação de tabelas e registro de rotas.
"""

from fastapi import FastAPI
from app.database import engine, Base
from app.routes.tasks import router as tasks_router

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="Laboratorio TaskAPI",
    description="Micro-API de To-Do List com suporte a CRUD, filtros e status",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir rotas de tarefas
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])


@app.get("/", tags=["root"])
def read_root() -> dict:
    """
    Endpoint raiz da API.
    
    Returns:
        dict: Mensagem de boas-vindas com informações sobre a API.
    """
    return {
        "message": "Bem-vindo à TaskAPI!",
        "docs": "/docs",
        "redoc": "/redoc"
    }