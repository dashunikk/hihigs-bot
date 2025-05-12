# version 1.0.1
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from config import TOKEN
from handlers import register_message_handlers
from utils import setup_logger
from handlers import set_commands
from db import async_create_table
from handlers.callbacks import callback_message, callback_start_tutor

async def main():
    """
    Основная функция для установки конфигурации бота.
    Для создания бота необходимо получить token в telegram https://t.me/BotFather
    и добавить полученный токен в файл .env
    создать папку log, в которую будут записываться логи от работы бота
    """

    #Экземпляры бота и диспетчеры
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    setup_logger(fname=__name__)

    # запуск команд
    await set_commands(bot)

    #Определение маршрутизации для диспетчера из handlers
    await register_message_handlers(dp)

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)

    # Регистрация обработчиков коллбеков
    await dp.callback_query_handler(callback_message, text = "callback_message")
    await dp.callback_query_handler(callback_start_tutor, text = "callback_start_tutor")

if __name__ == "__main__":
    try:
        asyncio.run(async_create_table())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("End Script")