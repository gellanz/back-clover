from database import solicitudes, magos, fetch_all, execute
from sqlalchemy import select, insert
import random


def generar_grimorio():
    numbers = [1, 2, 3, 4, 5]
    # probabilidades para cada numero de treboles. Solo uno de cada 100 sacarian un grimorio de 5 hojas
    weights = [0.15, 0.4, 0.3, 0.14, 0.01]
    return random.choices(numbers, weights)[0]


async def insertar_nuevo_mago(id):
    insert_new_mage_query = insert(magos).values(
        identificacion=id, treboles_grimorio=generar_grimorio()
    )
    await execute(insert_new_mage_query)


async def validar_existencia_solicitud(id: str):
    query = (
        select("*").select_from(solicitudes).where(solicitudes.c.identificacion == id)
    )
    if await fetch_all(query):
        return True
    return False
