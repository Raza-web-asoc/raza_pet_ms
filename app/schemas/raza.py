from pydantic import BaseModel
from typing import Optional

class RazaBase(BaseModel):
    nombre_raza: str
    id_especie: int
    historia: Optional[str] = None

class RazaCreate(RazaBase):
    pass

class RazaUpdate(RazaBase):
    pass

class RazaInDBBase(RazaBase):
    id_raza: int

    class Config:
        orm_mode = True

class Raza(RazaInDBBase):
    pass

class RazaInDB(RazaInDBBase):
    pass