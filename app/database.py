from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite
DATABASE_URL = "sqlite:///./tasks.db"

# Criar engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()