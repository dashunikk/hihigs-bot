__all__ = [
    "router",
]

from aiogram.filters import Command
from aiogram import Router
from sqlalchemy import select
from db import async_session, User
from .keyboard import keyboard_continue, keyboard_start  # импорт из клавиатур
from .callbacks import callback_message  # импорт из коллбека

#Создание экземпляра объекта Router
router = Router()

@router.message(Command("help"))
async def process_help_command(message):
    '''Команда help'''
    await message.answer("Помоги!", reply_markup=keyboard_continue)

@router.message(Command(commands=["start", "status"]))
async def process_start_command(message):
    '''Команда регистрации и справки'''
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

