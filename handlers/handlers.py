__all__ = [
    "register_message_handlers",
]

from aiogram import types, Router, filters, F
from sqlalchemy import select
from db import async_session, User
from .keyboard import keyboard_continue, keyboard_start  # импорт из клавиатур
from .callbacks import callback_message, callback_start_tutor  # импорт из коллбека

async def process_help_command(message):
    """Команда help"""
    await message.answer("Помоги!", reply_markup=keyboard_continue)

async def process_start_command(message: types.Message):
    """Команда регистрации и справки"""
    #Проверка на наличие пользователя в бд
    async with async_session() as session:
        query = select(User).where(message.from_user.id == User.user_id)
        result = await session.execute(query)
        #если пользователь в бд есть
        if result.scalars().all():
            info = "Чтобы продолжить, вызовите команду /status"
            await message.answer(info)
        #если пользователя нет в бд
        else:
            await  message.answer("Выберите роль", reply_markup=keyboard_start)


    await message.reply(f"{message.from_user.id}, {message.from_user.username}")

async def register_message_handlers(router: Router):
    """Маршрутизация обработчиков"""
    router.message.register(process_start_command, filters.Command(commands=["start", "status"]))
    router.callback_query.register(callback_message, F.data.endswith("_continue"))
    router.callback_query.register(callback_start_tutor), F.data.endswith("_tutor")