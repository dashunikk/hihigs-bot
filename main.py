# version 1.0.1
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
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
    # Инициализация базы данных
    await init_db()

    # Экземпляры бота и диспетчеры
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    setup_logger(fname=__name__)

    # Установка команд бота
    await set_commands(bot)

    # Регистрация обработчиков
    await register_message_handlers(dp)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(async_create_table())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")