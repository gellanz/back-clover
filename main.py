from fastapi import FastAPI, HTTPException, Path, Query, Body
from database import solicitudes, magos, fetch_all, execute, estado_enum
from sqlalchemy import select, delete, update, insert
from models import Solicitud
from schemas import NuevaSolicitud, TransaccionCompletada
from utils import insertar_nuevo_mago, validar_existencia_solicitud

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
    return NuevaSolicitud(message="Solicitud generada correctamente", data=solicitud)


@app.put("/solicitud/{id}")
async def update_solicitud(id: str, field: str, value: str | int):

    valid_fields = {
        "nombre",
        "apellido",
        "identificacion",
        "edad",
        "afinidad_magica",
        "estatus",
    }
    if field not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field: {field}")

    if not await validar_existencia_solicitud(id):
        raise HTTPException(status_code=404, detail=f"Identificador no encontrado")

    update_query = (
        update(solicitudes)
        .where(solicitudes.c.identificacion == id)
        .values({ field: value })
    )
    await execute(update_query)

    return TransaccionCompletada(
        message=f"Solicitud actualizada para el campo {field}", id=id
    )


@app.patch("/solicitud/{id}/estatus")
async def patch_item(id: str, value: str):
    print(value)
    update_query = (
        update(solicitudes)
        .where(solicitudes.c.identificacion == id)
        .values(estatus = value)
    )
    await execute(update_query)

    if value == "aprobada":
        await insertar_nuevo_mago(id)

    return TransaccionCompletada(
        message=f"Estatus de la solicitud actualizado a {value}", id=id
    )


@app.delete("/solicitud/{id}")
async def delete_item(id: str):
    delete_query = delete(solicitudes).where(solicitudes.c.identificacion == id)
    await execute(delete_query)
    return TransaccionCompletada(
        message=f"Mago con identificador {id} ha sido eliminado"
    )

# To run the application, use the command:
# uvicorn your_script_name:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")