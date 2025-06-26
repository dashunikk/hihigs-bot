__all__ = [
    "async_create_table",
    "async_sessionmaker",
]

import sqlite3
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
import logging
from .base import Base

engine = create_async_engine(
    url="sqlite+aiosqlite:///instance/sqlite.db",
    echo=True,  # Логирование SQL-запросов
    future=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def async_create_table() -> None:
    async with engine.begin() as conn:
        logging.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Tables created successfully")

# Синхронное подключение для обычных SQL-запросов
def get_db_connection():
    """Возвращает синхронное соединение с SQLite"""
    conn = sqlite3.connect('instance/sqlite.db')
    conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
    return conn