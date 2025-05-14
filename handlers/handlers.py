__all__ = [
    "register_message_handlers",
]

from aiogram import types, Router, filters, F
from sqlalchemy import select
from db import async_session, User
from .keyboard import keyboard_continue, keyboard_start  # импорт из клавиатур
from .callbacks import callback_message, callback_start_tutor, callback_insert_tutorcode, start_student # импорт из коллбека

# информация о статусе
status_string: str = """
UserId: {}
UserName: {}
"""

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

async def process_status_command(message: types.Message):
        """Команда регистрации и справки"""
        # Проверка на наличие пользователя в бд
        async with async_session() as session:
            query = select(User).where(message.from_user.id == User.user_id)
            result = await session.execute(query)
            user = result.scalar()
            # если пользователь в преподаватель
            if user.tutorcode:
                info = status_string + "Код преподавателя: {}"
                info = info.format(user.user_id, user.username, user.tutorcode)

            # если пользователь слушатель
            if user.subscribe:
                code = str(user.subscribe)
                info = status_string + "Преподаватель: {}"
                query = select(User).where(code == User.tutorcode)
                result = await session.execute(query)
                tutor = result.scalar()
                try:
                    info = info.format(user.user_id, user.username, tutor.username)
                except:
                    info = info.format(user.user_id, user.username)
            await message.answer(info)


async def register_message_handlers(router: Router):
    """Маршрутизация обработчиков"""
    router.message.register(process_start_command, filters.Command(commands=["start"]))
    router.message.register(process_status_command, filters.Command(commands=["status"]))
    router.callback_query.register(callback_message, F.data.endswith("_continue"))
    router.callback_query.register(callback_start_tutor, F.data.endswith("_tutor"))
    #router.callback_query.register(callback_start_student, F.data.endswith("_student"))
    router.callback_query.register(callback_insert_tutorcode, F.data.endswith("_student"))
    router.message.register(start_student, F.text.startswith("tutorcode-"))
