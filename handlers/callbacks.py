from aiogram.types import CallbackQuery
from aiogram import Router, F

from db import async_session

router = Router()

@router.callback_query(F.data == 'love_programming')
async def callback_message(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Я БОЛЬШЕ НЕ МОГУ")

@router.callback_query(F.data == 'favorite_teacher')
async def callback2_message(call: CallbackQuery):
    await call.answer()
    await call.message.answer("мой тоже :З")

@router.callback_query(F.data == 'life_without_python')
async def callback3_message(call: CallbackQuery):
    await call.answer()
    await call.message.answer("легко и просто")

    #TODO - два коллбек-ответа на кнопку слушатель/преподаватель
    #async with async_session() as session:
    #   """Что-то происходит"""
    #   insert_query = insert(User).values()
    #   await session.execute(insert_query)
    #   await session.commit()