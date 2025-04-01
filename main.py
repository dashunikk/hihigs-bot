# version1.0.0
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router

async def main():
    """
    Основная функция для установки конфигурации бота.
    Для создания бота необходимо получить token в telegram https://t.me/BotFather
    и добавить полученный токен в файл .env
    """

    #Экземпляры бота и диспетчеры
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    #Определение маршрутизации для диспетчера из handlers
    dp.include_routers(router)

    # Запуск бота в polling-режиме
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())