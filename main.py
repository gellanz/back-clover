from fastapi import FastAPI, HTTPException, Path, Query, Body
from database import solicitudes, magos, fetch_all, execute
from sqlalchemy import select
from models import Solicitud, Mago

app = FastAPI()


@app.get("/solicitudes")
async def get_solicitudes():
    select_query = (
        select("*")
        .select_from(solicitudes)
    )
    return await(fetch_all(select_query))


@app.get("/asignaciones")
async def get_asignaciones():
    select_query = (
        select("*")
        .select_from(magos)
    )
    return await(fetch_all(select_query))


# POST: Create a new item
@app.post("/solicitud", status_code=201)
async def create_item(item: Item):
    items.append(item)
    return item

# PUT: Update an existing item by ID
@app.put("/solicitud/{id}")
async def update_item(id: int):
    raise HTTPException(status_code=404, detail="Item not found")

# PATCH: Partially update an existing item by ID
@app.patch("/solicitud/{id}/estatus")
async def patch_item(id: int):

    raise HTTPException(status_code=404, detail="Item not found")

# DELETE: Delete an item by ID
@app.delete("/solicitud/{id}")
async def delete_item(id: int):
    raise HTTPException(status_code=404, detail="Item not found")

# To run the application, use the command:
# uvicorn your_script_name:app --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")