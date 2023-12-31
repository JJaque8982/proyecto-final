from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    #comprobacion de usuario
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_user(db=db, user=user)


@app.get("/user/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.delete("/users/{user_id}", response_model=schemas.UserDelete)
def delete_user(user_id: int , db: Session = Depends(get_db)):
    # Verifica si el usuario existe
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Elimina el usuario
    crud.delete_user(db=db, user_id=user_id)

    return {"detail":"Usuario eliminado satisfactoriamente"}

@app.post("/users/{user_id}/tareas/", response_model=schemas.Tarea)
def create_tarea_for_user(
    user_id: int, tarea: schemas.TareaCreate, db: Session = Depends(get_db)
):
    return crud.create_user_tarea(db=db, tarea=tarea, user_id=user_id)

#solicitud get para listar tareas completadas
@app.get("/tarea/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return db_user
#buscar tareas filtradas por estado segun el usuario 
@app.get("/tareas/{user_id}")
async def read_tareas(user_id: int, estado: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if estado:
        return db.query(models.Tarea).filter(models.Tarea.estado == True, models.Tarea.owner_id == user_id).offset(skip).limit(limit).all()
    else:
        return db.query(models.Tarea).filter(models.Tarea.estado == False, models.Tarea.owner_id == user_id).offset(skip).limit(limit).all()

@app.put("/tareas/{tarea_id}", response_model=schemas.Tarea)
def update_tarea(tarea_id: int, tarea_update: schemas.TareaUpdate, db: Session = Depends(get_db)):
    db_tarea = crud.update_tarea(db, tarea_id, tarea_update)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

@app.put("/tareas_estado/{tarea_id}", response_model=schemas.Tarea)
def update_tarea_estado(tarea_id: int, tarea_update: schemas.TareaEstadoUpdate, db: Session = Depends(get_db)):
    db_tarea = crud.update_tarea_estado(db, tarea_id, tarea_update)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea
    

#eliminar tareas
@app.delete("/tarea_delete/{tarea_id}", response_model=schemas.TareaDelete)
def delete_tarea(tarea_id: int , db: Session = Depends(get_db)):
    # Verifica si la tarea existe
    db_tarea = crud.get_tarea(db, tarea_id)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="tarea no encontrada")
    # Elimina la tarea
    crud.delete_tarea(db=db, tarea_id=tarea_id)
    return {"detail":"Tarea eliminado satisfactoriamente"}