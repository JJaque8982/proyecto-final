import pytest
from unittest.mock import MagicMock


from sqlalchemy.orm import Session
from sql_app.crud import create_user, create_user_tarea

from sql_app import models, schemas
from datetime import date

#app = FastAPI()
#client = TestClient(app)
def test_create_user_tarea():

    db = Session()
    # Para que no de problemas hay que hacerlo con try except
    try:
        # Arreglo
        tarea = schemas.TareaCreate(name="test tarea",
                                    titulo="test titulo", 
                                    description="test description",
                                    fecha_ven="2023-10-30",
                                    activa="true")
        user = schemas.UserCreate(email="test@example.com", 
                                password="password123")
        created_user = create_user(db, user)

        # Metemos todo en created_tarea, osea la sesion, tarea y el id de usuario
        created_tarea = create_user_tarea(db, tarea, created_user.id)

        # Asserts
        assert isinstance(created_tarea, models.Tarea)
        assert created_tarea.titulo == "test tarea"
        assert created_tarea.descripcion == "test description"
        assert created_tarea.fecha_ven == "2023-10-30"
        assert created_tarea.estado == "true"
    except:
         # rollback() porque me estaba dando problemas
         db.rollback()
    finally:
         # Y cerramos la conexión
         db.close()