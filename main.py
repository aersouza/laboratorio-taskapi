from fastapi import FastAPI

# Inicializamos a nossa API
app = FastAPI(title="API de Agendamento de Aulas")

# Criamos a nossa primeira Rota
@app.get("/")
def ola_mundo():
    return {"mensagem": "Olá! A API de Agendamento de Aulas está online!"}