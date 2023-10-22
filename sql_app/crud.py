from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tareas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tarea).offset(skip).limit(limit).all()



def create_user_tarea(db: Session, tarea: schemas.TareaCreate, user_id: int):
    db_tarea = models.Tarea(**tarea.dict(), owner_id=user_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea) 
    return db_tarea

#actualizar datos de tarea
def update_tarea(db: Session, tarea_id: int, tarea_update: schemas.TareaUpdate):
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()

    if db_tarea is None:
        return None  # Opcional: manejar el caso en el que la tarea no existe
    for field, value in tarea_update.dict().items():
        setattr(db_tarea, field, value)

    db.commit()
    db.refresh(db_tarea)
    return db_tarea

#eliminar usuario
def delete_user(db: Session, user_id: int):
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user_to_delete is None:
        return None  # Opcional: manejar el caso en el que el usuario no existe
    db.delete(user_to_delete)
    db.commit()
    return user_to_delete


#actualizar estado de tarea
def update_tarea_estado(db: Session, tarea_id: int, tarea_update: schemas.TareaEstadoUpdate):
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()

    if db_tarea is None:
        return None  # Opcional: manejar el caso en el que la tarea no existe
    for field, value in tarea_update.dict().items():
        setattr(db_tarea, field, value)

    db.commit()
    db.refresh(db_tarea)
    return db_tarea
#eliminar tareas
def delete_tarea(db: Session, tarea_id: int):
    tarea_to_delete = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    
    if tarea_to_delete is None:
        return None  # Opcional: manejar el caso en el que el usuario no existe
    db.delete(tarea_to_delete)
    db.commit()
    return tarea_to_delete
#buscar tareas filtradas por estado
def get_tarea(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Tarea).filter(models.Tarea.owner_id == user_id).offset(skip).limit(limit).first()
