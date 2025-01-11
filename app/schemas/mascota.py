from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class MascotaBase(BaseModel):
    nombre_mascota: str
    id_especie: int
    id_raza: int
    sexo: str
    fecha_nacimiento: date
    nombre_raza: Optional[str] = None
    nombre_especie: Optional[str] = None

class MascotaCreate(MascotaBase):
    pass

class MascotaUpdate(MascotaBase):
    pass

class MascotaInDBBase(MascotaBase):
    id_mascota: int
    id_usuario: int
    fecha_registro: Optional[datetime] = None

    class Config:
        orm_mode = True

class Mascota(MascotaInDBBase):
    pass

class MascotaInDB(MascotaInDBBase):
    pass