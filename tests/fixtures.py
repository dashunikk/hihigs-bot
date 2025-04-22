import pytest
from unittest.mock import AsyncMock
from aiogram.types import Message
from aiogram import Router

# Фикстуры в pytest позволяют выносить в отдельные функции типовые действия
# например: настройка тестового окружения, создание тестовых данных, выполнение завершающие действия
# https://habr.com/ru/articles/731296/

@pytest.fixture
def mock_message():
    mock_msg = AsyncMock(spec=Message)
    mock_msg.reply = AsyncMock()
    mock_msg.from_user.id = 123
    mock_msg.from_user.username = "test_user"
    return mock_msg

@pytest.fixture
def mock_router():
    """Mock роутер"""
    router = Router()
    return router
