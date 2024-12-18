from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class MascotaBase(BaseModel):
    nombre_mascota: str
    id_especie: int
    id_raza: int
    sexo: str
    fecha_nacimiento: date
    id_usuario: int

class MascotaCreate(MascotaBase):
    pass

class MascotaUpdate(MascotaBase):
    pass

class MascotaInDBBase(MascotaBase):
    id_mascota: int
    fecha_registro: Optional[datetime] = None

    class Config:
        orm_mode = True

class Mascota(MascotaInDBBase):
    pass

class MascotaInDB(MascotaInDBBase):
    pass