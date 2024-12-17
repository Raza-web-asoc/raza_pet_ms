import sys
import os
from fastapi import FastAPI

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import init_db

app = FastAPI()

init_db()

@app.get("/")
def read_root():
    return {"message": "¡Hola! FastAPI está corriendo correctamente."}
