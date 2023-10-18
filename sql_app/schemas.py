from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import date

class TareaBase(BaseModel):
    titulo: str
    descripcion: Union[str, None] = None
    fecha_ven: date
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

#actualizar tareas
class TareaUpdate(BaseModel):
    titulo: Union[str, None] = None
    descripcion: Union[str, None] = None
    fecha_ven: Union[date, None] = None
    estado: Union[bool, None] = None
    
class TareaEstadoUpdate(BaseModel):
       estado: Union[bool, None] = None

#filtrar tareas segun su estado
class TareaFilter(BaseModel):
    estado: Optional[bool] = None  

class TareaDelete(BaseModel):
    detail: str

  