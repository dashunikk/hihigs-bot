__all__ = [
    "User",
    "Base",
]

# Про ORM-паттерн асинхронного sqlalchemy и модели
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm

# декларативная модель базы данных python
# https://metanit.com/python/database/3.2.php

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DATE, Integer, VARCHAR, Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


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

# Инициализация движка и сессии
engine = create_async_engine(
    "sqlite+aiosqlite:///instance/sqlite.db",
    echo=True  # Логирование SQL-запросов
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    """Создает все таблицы при старте приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_vm_data(session: AsyncSession, user_id: int, ip: str, username: str, password: str):
    """Сохраняет данные VM в базу"""
    user = await session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    user.vm_ip = ip
    user.vm_username = username
    user.vm_password = password
    await session.commit()