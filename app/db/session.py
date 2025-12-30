from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.core.config import settings

# Crear engine de SQLAlchemy
engine: create_engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# Crear SessionLocal
SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base: declarative_base = declarative_base()


# Dependency para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



