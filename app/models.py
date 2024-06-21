from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints


class Solicitud(BaseModel):
    nombre: Annotated[str, StringConstraints(pattern='^[a-zA-Z]+$', max_length=20)] = Field(..., description="Nombre: solo letras, máximo 20 caracteres.")
    apellido: Annotated[str, StringConstraints(pattern='^[a-zA-Z]+$', max_length=20)] = Field(..., description="Apellido: solo letras, máximo 20 caracteres.")
    identificacion: Annotated[str, StringConstraints(pattern='^[a-zA-Z0-9]+$', max_length=10)] = Field(..., description="Identificación: números y letras, máximo 10 caracteres.")
    edad: Annotated[int, Field(strict=True, gt=15, lt=99, description="Edad del mago aspirante, generalmente hacen la solicitud a los 15")]
    afinidad_magica: Literal['Oscuridad', 'Luz', 'Fuego', 'Agua', 'Viento', 'Tierra'] = Field(..., description="Afinidad Mágica")
    #estatus: Literal['Procesando', 'Aprobada', 'Denegada'] = Field(..., description="Estatus de la solicitud")

class Mago(BaseModel):
    identificacion: Annotated[str, StringConstraints(pattern='^[a-zA-Z0-9]+$', max_length=10)] = Field(..., description="Identificación: números y letras, máximo 10 caracteres.")
    treboles_grimorio: Annotated[int, Field(strict=True, gt=0, lt=6)]