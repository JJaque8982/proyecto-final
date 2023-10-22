import json
from fastapi.testclient import TestClient

from .main import app
from sql_app import schemas

client = TestClient(app)


def test_create_user_success():
    # Datos de usuario de prueba
    user_data = {
        "email": "test@example.com",
        "password": "password123",
    }

    # Realiza una solicitud POST para crear un usuario
    response = client.post("/users/", json=user_data)

    # Verifica que la respuesta tenga un código de estado 200 (OK)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario que coincide con la estructura de User
    user = response.json()
    assert "id" in user  # El usuario debe tener un ID
    assert user["email"] == user_data["email"]
    assert user["is_active"] is True  # Asumiendo que el usuario se crea activo


def test_create_user_duplicate_email():
    # Datos de usuario de prueba
    user_data = {
        "email": "test@example.com",
        "password": "password123",
    }

    # Crea un usuario con el mismo email en la base de datos para simular un duplicado
    create_duplicate_user_in_database(user_data["email"])

    # Realiza una solicitud POST para crear un usuario con el mismo email
    response = client.post("/users/", json=user_data)

    # Verifica que la respuesta tenga un código de estado 400 (conflicto)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email ya registrado"}

# Función para crear un usuario duplicado en la base de datos (simulación)
def create_duplicate_user_in_database(email):
    user_data = {
        "email": email,
        "password": "password123",
    }

def test_delete_user_success():
    # Supongamos que tienes un usuario en tu base de datos de prueba con user_id=1
    user_id = 1
    response = client.delete(f"/users/{user_id}")
    
    # Verifica que la respuesta tenga un código de estado 200 (OK)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario que coincide con la estructura de UserDelete
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Usuario eliminado satisfactoriamente"

def test_delete_user_not_found():
    # Supongamos que intentas eliminar un usuario que no existe (user_id=999)
    user_id = 999
    response = client.delete(f"/users/{user_id}")

    # Verifica que la respuesta tenga un código de estado 404 (No encontrado)
    assert response.status_code == 404

    # Verifica que la respuesta sea un diccionario que coincide con la estructura de HTTPException
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Usuario no encontrado"

def test_create_tarea_for_user_true():
    # Crear un usuario de prueba
    user_data = {
        "email": "testusertarea1@example.com",
        "password": "password123",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Datos de la tarea a crear
    tarea_data = {
        "titulo": "Tarea false",
        "descripcion": "Esta es una tarea de prueba",
        "fecha_ven": "2023-12-31",
        "estado": False
    }

    # Realizar una solicitud POST para crear una tarea para el usuario
    response = client.post(f"/users/{user_id}/tareas/", json=tarea_data)

    # Verificar que la respuesta tenga un código de estado 200 (éxito)
    assert response.status_code == 200

    # Verificar que la respuesta incluya los datos de la tarea creada
    tarea = response.json()
    assert "id" in tarea
    assert tarea["titulo"] == tarea_data["titulo"]
    assert tarea["descripcion"] == tarea_data["descripcion"]
    assert tarea["fecha_ven"] == tarea_data["fecha_ven"]
    assert tarea["estado"] == tarea_data["estado"]
def test_create_tarea_for_user_false():
    # Crear un usuario de prueba
    user_data = {
        "email": "testusertarea0@example.com",
        "password": "password123",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Datos de la tarea a crear
    tarea_data = {
        "titulo": "Tarea true",
        "descripcion": "Esta es una tarea de prueba",
        "fecha_ven": "2023-12-31",
        "estado": True
    }
    # Realizar una solicitud POST para crear una tarea para el usuario
    response = client.post(f"/users/{user_id}/tareas/", json=tarea_data)

    # Verificar que la respuesta tenga un código de estado 200 (éxito)
    assert response.status_code == 200

    # Verificar que la respuesta incluya los datos de la tarea creada
    tarea = response.json()
    assert "id" in tarea
    assert tarea["titulo"] == tarea_data["titulo"]
    assert tarea["descripcion"] == tarea_data["descripcion"]
    assert tarea["fecha_ven"] == tarea_data["fecha_ven"]
    assert tarea["estado"] == tarea_data["estado"]


#get tareas  por estado true/false  
def test_get_tareas_true():

    response = client.get("/tareas/2?estado=true")
    assert response.status_code == 200
    print(json.dumps(response.json(), indent=4))
    assert response.json()    

def test_get_tareas_false():

    response = client.get("/tareas/1?estado=false")
    assert response.status_code == 200
    print(json.dumps(response.json(), indent=4))
    assert response.json()        

def test_update_tarea_estado_success():
 
    tarea_update_data = {
        "estado": True  # Supongamos que se quiere cambiar el estado a 'True'
    }
    response = client.put(f"/tareas_estado/1", json=tarea_update_data)
    
    # Verifica que la respuesta tenga un código de estado 200 (OK)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario que coincide con la estructura de Tarea
    response_data = response.json()

    # Verifica que el estado de la tarea se haya actualizado correctamente
    assert response_data["estado"] == True  # Debería ser True según los datos de prueba

def test_update_tarea_estado_not_found():
    # Supongamos que deseas actualizar una tarea con un ID que no existe (por ejemplo, ID 9999).
    tarea_id = 9999
    tarea_update_data = {
        "estado": True  # Datos de actualización de estado
    }

    # Realiza una solicitud PUT para actualizar la tarea con un ID que no existe
    response = client.put(f"/tareas_estado/{tarea_id}", json=tarea_update_data)

    # Verifica que la respuesta tenga un código de estado 404 (Not Found)
    assert response.status_code == 404

    # Verifica que la respuesta incluya un mensaje de error específico (opcional)
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Tarea no encontrada"

def test_update_tarea_success():
    # Datos de tarea de prueba para actualizar
    tarea_data = {
        "titulo": "Nueva tarea",
        "descripcion": "Descripción de la tarea",
        "fecha_ven": "2023-12-31",
        "estado": True
    }

    # Realiza una solicitud PUT para actualizar la tarea
    response = client.put("/tareas/1", json=tarea_data)

    # Verifica que la respuesta tenga un código de estado 200 (OK)
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario que coincide con la estructura de Tarea
    response_data = response.json()

    # Verifica que los datos de la tarea se hayan actualizado correctamente
    assert response_data["titulo"] == "Nueva tarea"
    assert response_data["descripcion"] == "Descripción de la tarea"
    assert response_data["fecha_ven"] == "2023-12-31"
    assert response_data["estado"] is True

def test_update_tarea_not_found():
    # Datos de tarea de prueba para actualizar (pueden ser los mismos que el test de éxito)
    tarea_data = {
        "titulo": "Nueva tarea",
        "descripcion": "Descripción de la tarea",
        "fecha_ven": "2023-12-31",
        "estado": True
    }

    # Realiza una solicitud PUT para actualizar una tarea que no existe (tarea_id 999 no existe)
    response = client.put("/tareas/999", json=tarea_data)

    # Verifica que la respuesta tenga un código de estado 404 (Not Found)
    assert response.status_code == 404

    # Verifica que la respuesta incluya un mensaje de error específico (opcional)
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Tarea no encontrada"
    
def test_delete_tarea_success():
    # Realiza una solicitud DELETE para eliminar la tarea.
    response = client.delete(f"/tarea_delete/2")

    # Verifica que la respuesta tenga un código de estado 200 (Éxito).
    assert response.status_code == 200

    # Verifica que la respuesta sea un diccionario que coincide con la estructura de respuesta.
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"].lower() == "tarea eliminado satisfactoriamente"  # Convierte a minúsculas antes de comparar
def test_delete_tarea_not_found():
    # Supongamos que intentas eliminar una tarea que no existe (tarea_id=999)
    response = client.delete(f"/tarea_delete/999")

    # Verifica que la respuesta tenga un código de estado 404 (No encontrado)
    assert response.status_code == 404

    # Verifica que la respuesta sea un diccionario que coincide con la estructura de HTTPException
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"].lower() == "tarea no encontrada"

