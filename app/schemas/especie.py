from pydantic import BaseModel

class EspecieBase(BaseModel):
    nombre_especie: str

class EspecieCreate(EspecieBase):
    pass

class EspecieUpdate(EspecieBase):
    pass

class EspecieInDBBase(EspecieBase):
    id_especie: int

    class Config:
        orm_mode = True

class Especie(EspecieInDBBase):
    pass

class EspecieInDB(EspecieInDBBase):
    pass