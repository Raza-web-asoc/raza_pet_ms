from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        engine.connect()
        print("Conectadooooooo")
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
    
