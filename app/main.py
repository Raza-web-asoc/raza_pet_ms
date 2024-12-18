import sys
import os
from fastapi import FastAPI

# Añadir el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.controllers import mascota, especie, raza
from app.db.base import init_db

app = FastAPI()

init_db()

app.include_router(mascota.router, prefix="/mascotas", tags=["mascotas"])
app.include_router(especie.router, prefix="/especies", tags=["especies"])
app.include_router(raza.router, prefix="/razas", tags=["razas"])

@app.get("/")
def read_root():
    return {"message": "¡Hola! FastAPI está corriendo correctamente."}
