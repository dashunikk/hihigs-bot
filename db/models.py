__all__ = [
    "User",
    "Base",
]

# Про ORM-паттерн асинхронного sqlalchemy и модели
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm

# декларативная модель базы данных python
# https://metanit.com/python/database/3.2.php

from sqlalchemy.orm import DeclarativeBase
from .base import Base
from sqlalchemy import Column, DATE, Integer, VARCHAR, Text
from sqlalchemy.ext.asyncio import create_async_engine
from db.engine import get_db_connection


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_table"
    user_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), nullable=False)
    tutorcode = Column(VARCHAR(6), unique=False)
    subscribe = Column(VARCHAR(6), unique=False)
    extra = Column(Text, unique=False)
    vm_ip = Column(VARCHAR(45), nullable=True)
    vm_username = Column(VARCHAR(50), nullable=True)
    vm_password = Column(VARCHAR(100), nullable=True)

async def init_db():
    """Инициализация базы данных и создание таблиц"""
    # Создаем асинхронный движок для SQLite
    engine = create_async_engine(
        "sqlite+aiosqlite:///instance/sqlite.db",
        echo=True  # Включаем логирование SQL-запросов для отладки
    )

    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#это я из файла дб перекинула. нужно исправить...
def save_user(user_id: int, username: str, tutorcode=None, subscribe=None):
    """Сохраняет пользователя"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, tutorcode, subscribe)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, tutorcode, subscribe))
        conn.commit()

def save_vm_data(user_id: int, address: str, username: str, password: str):
    """Сохраняет данные VM"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO vm_connections (user_id, vm_address, vm_username, vm_password)
            VALUES (?, ?, ?, ?)
        ''', (user_id, address, username, password))
        conn.commit()

def get_vm_data(user_id: int):
    """Получает данные VM"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT vm_address, vm_username, vm_password 
            FROM vm_connections 
            WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchone()

def get_user_role(user_id: int):
    """Получает роль пользователя"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT tutorcode, subscribe FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()