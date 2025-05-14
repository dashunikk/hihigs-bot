import logging
import string
from random import choices
from aiogram.types import CallbackQuery
from sqlalchemy import insert
from db import async_session, User

async def callback_message(callback:  CallbackQuery):
    """Ответ на кнопку"""
    await callback.message.answer("Успешно!")

async def callback_start_tutor(callback: CallbackQuery):
    """Регистрация преподавателя"""

    async with async_session() as session:
        chars = string.ascii_letters + string.digits + string.punctuation
        new_user = {
            "user_id": callback.from_user.id,
            "username": callback.from_user.username,
            "tutorcode": "".join(choices(chars, k=6))
        }
        insert_query = insert(User).values(new_user)
        await session.execute(insert_query)
        await session.commit()
        await callback.message.answer("Пользователь добавлен!")
        logging.info(f"Пользователь {callback.from_user.username} добавлен в базу данных с ролью преподаватель!")

async def callback_insert_tutorcode(callback: CallbackQuery):
    """Регистрация слушателя. Ввод кода"""
    await callback.message.answer("Введите код преподавателя (в формате tutorcode-CODE):")

async def start_student(message):
    """Регистрация слушателя"""
    async with async_session() as session:
        new_user = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "subscribe": str(message.text.split("-")[1])
        }
        insert_query = insert(User).values(new_user)
        await session.execute(insert_query)
        await session.commit()
        await message.answer("Пользователь добавлен!")
        logging.info(f"Пользователь {message.from_user.username} добавлен в базу данных с ролью слушатель!")

