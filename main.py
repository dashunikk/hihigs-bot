# version 1.0.1
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router as router_handlers
from utils import setup_logger
from handlers import set_commands
from handlers.callbacks import router as router_callbacks


async def main():
    """
    Основная функция для установки конфигурации бота.
    Для создания бота необходимо получить token в telegram https://t.me/BotFather
    и добавить полученный токен в файл .env
    """

    #Экземпляры бота и диспетчеры
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    setup_logger(fname=__name__)

    # запуск команд
    await set_commands(bot)

    #Определение маршрутизации для диспетчера из handlers
    dp.include_routers(router_handlers, router_callbacks)

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

