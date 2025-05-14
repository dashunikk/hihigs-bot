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
    await callback.message.answer("Вы выбрали роль преподавателя!")

    async with async_session() as session:
        """Что-то происходит"""
        chars = string.ascii_letters + string.digits + string.punctuation
        new_user = {
            "user_id": callback.from_user.id,
            "username": callback.from_user.username,
            "tutorcode": "".join(choices(chars, k=6))
        }
        insert_query = insert(User).values()
        await session.execute(insert_query)
        await session.commit()
        await callback.message.answer("Пользователь добавлен!")
        logging.info(f"Пользователь {callback.from_user.username} добавлен в базу данных с ролью преподаватель!")

async def callback_start_student(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали роль студента!")

