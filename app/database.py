"""
Módulo de configuração do banco de dados.

Este módulo configura a conexão SQLAlchemy com SQLite,
cria a engine, sessão local e base declarativa para modelos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite
DATABASE_URL = "sqlite:///./tasks.db"

# Criar engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Criar factory de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Dependência do FastAPI para obter sessão do banco de dados.
    
    Yields:
        Session: Sessão do banco de dados.
    
    Example:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()