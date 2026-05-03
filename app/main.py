from fastapi import FastAPI
from app.database import engine, Base
from app.routes.tasks import router as tasks_router

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Laboratorio TaskAPI", description="Micro-API de To-Do List", version="1.0.0")

# Incluir rotas
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à TaskAPI!"}