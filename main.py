# API REST: Interfaz de Programacion de Aplicaciones para compartir recursos

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from typing import List, Optional

# Inicializamos una variable donde tendra todas las caracteristicas de una API REST
app = FastAPI()

# Aca definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int


# Simularemos una base de datos
cursos_db = []

# CRUD: Read (Lectura) GET ALL: Leeremos todos los cursos que haya en la db
@app.get("/cursos", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create (escribir) POST: agregaremos un nuevo recurso a nuestra base de datos
@app.post("/cursos", response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4())  # Usamos UUID para generar un ID unico e irrepetible
    cursos_db.append(curso)
    return curso  # Debes retornar el curso creado

# CRUD: Read (lectura) GET (individual): Leeremos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)  # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


# CRUD: Update (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)  # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso)
    cursos_db[index] = curso_actualizado  # Aquí faltaba asignar el curso actualizado
    return curso_actualizado


# CRUD: Delete (borrado/baja) DELETE: Eliminaremos un recurso que coincida con el ID que mandemos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)  # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso