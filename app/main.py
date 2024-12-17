from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# Configuración de la base de datos
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "rootpassword")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# Conexión con la base de datos
engine = create_engine(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "¡Hola! FastAPI está corriendo correctamente."}
