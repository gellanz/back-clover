from pydantic import BaseModel
from .models import Solicitud


class NuevaSolicitud(BaseModel):
    status_code: int = 200
    message: str
    data: Solicitud


class TransaccionCompletada(BaseModel):
    status_code: int = 200
    message: str
    id: str
