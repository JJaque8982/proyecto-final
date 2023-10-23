# Proyecto Final Python 2023

proyecto creado a base del conocimiento adquirido en el curso de python desarrollado durante los meses de septiembre-octubre. 
el desarrollo esta basado en el tutorial de fastapi obtenido de la ruta https://fastapi.tiangolo.com/tutorial/sql-databases/ ademas de la rúbrica de evaluación, la cual trae los siguientes items a calificar:

- Creación de Tareas
- Visualización de Tareas
- Edición y Eliminación de Tareas
- Marcado de Tareas como Completadas
- Cobertura de Código en Pruebas

## Authors

-mrjake
```https://github.com/JJaque8982
```
## Deployment
para empezar este desarrollo esta trabajado con las siguientes librerias las cuales deben estar previamente instaladas:

Instalar las librerias:
```FastAPI
    pip  install "fastapi[all]"
```
```uvicorn
    pip install "uvicorn[standard]"
```
```coverage
    pip install coverage
```
```pydantic
    pip install pydantic
```
```pytest
    pip install pytest 
```
```SQLAlchemy
    pip install sqlalchemy
```

teniendo todo instalado,seguiremos segun la creacion de su estructura similar a la presentada en el tutorial de fastapi para basarnos:
proyecto-final
    └── sql_app
            ├── __init__.py
            ├── crud.py
            ├── database.py
            ├── main.py
            ├── models.py
            ├── schemas.py
            └── test_main.py

Desde aquí ejecutaremos las siguientes lineas de comandos:

Inicializamos el servidor:
uvicorn sql_app.main:app --reload
Esto nos permite probar los endpoints creados con FastAPI
en la url: 127.0.0.1/8000/docs la que nos presentara la Interfaz con la que debemos trabajar.

para los test unitarios debemos ejecutar los siguientes comandos:

```Ejecutamos el comando coverage para realizar los test unitarios:
    coverage run -m pytest
```
```Ejecutamos el comando coverage, en este caso crearemos un registro html 
    coverage html
```

La ruta del archivo debería ser:
proyecto-final/htmlcov/index.html
Al abrirlo debería verse de la siguiente manera:
```
Coverage report: 97%Show/hide keyboard shortcuts
filter...
coverage.py v7.3.1, created at 2023-10-23 17:37 -0300

Module	        statements	missing	excluded	coverage
sql_app\__init__.py	 0	        0       	0	100%
sql_app\database.py	 7	        0       	0	100%
sql_app\models.py	 19     	0	        0	100%
sql_app\schemas.py   38     	0       	0	100%
sql_app\test_main.py 115        0	        0	100%
sql_app\crud.py	     57	        4	        0	93%
sql_app\main.py	     61	        6	        0	90%
Total	             297	    10      	0	97%
coverage.py v7.3.1, created at 2023-10-23 17:37 -0300
```