from pydantic import BaseModel
from typing import List, Union

class TareaBase(BaseModel):
    titulo: str
    descripcion: Union[str, None] = None
    
    estado:bool

class TareaCreate(TareaBase):
     pass
   

class Tarea(TareaBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    Tareas: List[Tarea] = []

    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    detail: str