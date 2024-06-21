from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Select,
    Insert,
    Update,
    Delete,
    CursorResult,
    Table,
    MetaData,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Any
import enum
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()

metadata = MetaData()


# Tablas
class AfinidadMagicaEnum(str, enum.Enum):
    Oscuridad = "Oscuridad"
    Luz = "Luz"
    Fuego = "Fuego"
    Agua = "Agua"
    Viento = "Viento"
    Tierra = "Tierra"


class estado_enum(str, enum.Enum):
    procesando = "procesando"
    aprobada = "aprobada"
    denegada = "denegada"


solicitudes = Table(
    "solicitudes",
    metadata,
    Column("nombre", String(20), nullable=False),
    Column("apellido", String(20), nullable=False),
    Column("identificacion", String(10), unique=True, nullable=False),
    Column("edad", Integer, nullable=False),
    Column("afinidad_magica", String, nullable=False),
    Column("estatus", Enum(estado_enum), nullable=False),
    schema="ia",
)

magos = Table(
    "magos",
    metadata,
    Column("nombre", String(20), nullable=False),
    Column("apellido", String(20), nullable=False),
    Column("identificacion", String(10), unique=True, nullable=False),
    Column("edad", Integer, nullable=False),
    Column("afinidad_magica", Enum(AfinidadMagicaEnum), nullable=False),
    Column("treboles_grimorio", Integer, nullable=False),
    schema="ia",
)


# Abstracciones para ejecturar queries
async def fetch_all(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return [result._asdict() for result in cursor.all()]


async def execute(query: Delete | Insert | Update) -> None:
    async with engine.begin() as conn:
        await conn.execute(query)
