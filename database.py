from sqlalchemy import Column, Integer, String, Enum, Select, Insert, Update, Delete, CursorResult, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Any
import enum

DATABASE_URL = "postgresql+asyncpg://username:password@localhost:5432/mydatabase"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

# Tablas
class AfinidadMagicaEnum(enum.Enum):
    Oscuridad = "Oscuridad"
    Luz = "Luz"
    Fuego = "Fuego"
    Agua = "Agua"
    Viento = "Viento"
    Tierra = "Tierra"

solicitudes = Table(
    "solicitudes",    
    Column("nombre", String(20), nullable=False),
    Column("apellido", String(20), nullable=False),
    Column("identificacion", String(10), unique=True, nullable=False),
    Column("edad", Integer, nullable=False),
    Column("afinidad_magica", Enum(AfinidadMagicaEnum), nullable=False),
    schema="ia"
)

magos = Table(
    "magos",
    Column("nombre", String(20), nullable=False),
    Column("apellido", String(20), nullable=False),
    Column("identificacion", String(10), unique=True, nullable=False),
    Column("edad", Integer, nullable=False),
    Column("afinidad_magica", Enum(AfinidadMagicaEnum), nullable=False),
    Column("treboles_grimorio", Integer, nullable=False),
    schema="ia"
)

# Abstracciones para ejecturar queries
async def fetch_all(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.exucute(select_query)
        return [result._asdict() for result in cursor.all()]


async def execute(select_query: Delete | Insert | Update) -> None:
    async with engine.begin() as conn:
        await conn.exucute(select_query)
