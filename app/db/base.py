from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
from app.db.models import Especie, Raza, Mascota  # Importar los modelos

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    try:
        engine.connect()
        print("Conectadooooooo")
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
        
    Base.metadata.create_all(bind=engine)
