from gc import callbacks

import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram import Router

# Фикстуры в pytest позволяют выносить в отдельные функции типовые действия
# например: настройка тестового окружения, создание тестовых данных, выполнение завершающие действия
# https://habr.com/ru/articles/731296/

@pytest.fixture
def mock_bot():
    """Mock бот"""
    with patch("main.Bot") as mock_bot_cls:
        mock_bot_instance = AsyncMock()
        mock_bot_cls.return_value =mock_bot_instance
        yield mock_bot_instance


@pytest.fixture
def mock_set_my_commands():
    """"Mock создание меню"""
    with patch("main.set_commands", new_callable=AsyncMock) as mock:
        yield mock_set_my_commands

@pytest.fixture
def mock_setup_logger():
   """"Mock логгер"""
   with patch("main.setup_logger", new_callable=AsyncMock) as mock:
       yield mock_setup_logger

@pytest.fixture
def mock_dispatcher():
    """Mock диспетчер"""
    with patch("main.Dispatcher") as mock_dispatcher_cls:
      mock_dispatcher_instance = AsyncMock()
      mock_dispatcher_instance.start_polling = AsyncMock()
      mock_dispatcher_instance.include_routers = AsyncMock()
      mock_dispatcher_cls.return_value = mock_dispatcher_instance
      yield mock_dispatcher_instance

@pytest.fixture
def mock_message():
    """Mock сообщение"""
    mock_msg = AsyncMock(spec=Message)
    mock_msg.answer =AsyncMock()
    mock_msg.call = AsyncMock()
    mock_msg.from_user = AsyncMock()
    mock_msg.from_user.id = AsyncMock()
    mock_msg.from_user.username = AsyncMock()
    mock_msg.message = AsyncMock()
    mock_msg.message.answer = AsyncMock()

    mock_message.reply = AsyncMock()
    return mock_msg

# @pytest.fixture
# def mock_callback_query():
#     """Mock CallbackQuery"""
#     mock_call = AsyncMock(spec=CallbackQuery)
#     mock_call.message = AsyncMock()
#     mock_call.answer = AsyncMock()
#     return mock_call


@pytest.fixture
def mock_routers():
    """Mock роутер"""
    router = Router()
    router_handlers = AsyncMock()
    router_callbacks = AsyncMock()
    return router

@pytest.fixture
def mock_router_handlers():
    """Mock роутер"""
    router = Router()
    return router

@pytest.fixture
def mock_router_callbacks():
    """Mock роутер"""
    router = Router()
    return router