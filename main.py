from fastapi import FastAPI, HTTPException, Path, Query, Body
from database import solicitudes, magos, fetch_all, execute
from sqlalchemy import select, delete, update, insert
from models import Solicitud, Mago

app = FastAPI()


@app.get("/solicitudes")
async def get_solicitudes():
    select_query = select("*").select_from(solicitudes)
    return await fetch_all(select_query)


@app.get("/asignaciones")
async def get_asignaciones():
    select_query = select("*").select_from(magos)
    return await fetch_all(select_query)


# POST: Crear solicitud
@app.post("/solicitud")
async def crear_solicitud(solicitud: Solicitud):
    insert_query = insert(solicitudes).values(
        nombre=solicitud.nombre,
        apellido=solicitud.apellido,
        identificacion=solicitud.identificacion,
        edad=solicitud.edad,
        afinidad_magica=solicitud.afinidad_magica,
        estatus="procesando",
    )
    await execute(insert_query)


# PUT: Actualizar solicitud
@app.put("/solicitud/{id}")
async def update_solicitud(id: int, field: str, value: str | int):

    valid_fields = {"nombre", "apellido", "identificacion", "edad", "afinidad_magica", "estatus"}
    if field not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field: {field}")

    update_query = (
        update(solicitudes)
        .values(solicitudes.c.field == value)
        .where(solicitudes.c.identificacion == id)
    )
    await execute(update_query)

    # raise HTTPException(status_code=404, detail="Item not found")


# PATCH: Partially update an existing item by ID
@app.patch("/solicitud/{id}/estatus")
async def patch_item(id: int, value: str):
    update_query = (
        update(solicitudes)
        .values(solicitudes.c.estatus == value)
        .where(solicitudes.c.identificacion == id)
    )
    await execute(update_query)

    # raise HTTPException(status_code=404, detail="Item not found")


# DELETE: Delete an item by ID
@app.delete("/solicitud/{id}")
async def delete_item(id: int):
    delete_query = delete(solicitudes).where(solicitudes.c.identificacion == id)
    await execute(delete_query)
    # raise HTTPException(status_code=404, detail="Item not found")


# To run the application, use the command:
# uvicorn your_script_name:app --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
