# version 1.0.1
import asyncio
import logging

from aiogram import Bot, Router, Dispatcher, types
from config import TOKEN
from handlers import register_message_handlers
from utils import setup_logger
from handlers import set_commands
from db.models import init_db
from db import async_create_table

async def main():
    """
    Основная функция для установки конфигурации бота.
    """
    await async_create_table()
    # Инициализация базы данных
    await init_db()

    # Экземпляры бота и диспетчеры
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    setup_logger(fname=__name__)
    router = Router()

    # Установка команд бота
    await set_commands(bot)

    # Регистрация обработчиков
    await register_message_handlers(router)

    # Подключаем роутер к диспетчеру
    dp.include_router(router)

    # Запуск бота
    await dp.start_polling(bot)

async def startup():
    await async_create_table()
    await main()

if __name__ == "__main__":
    try:
        asyncio.run(startup())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")