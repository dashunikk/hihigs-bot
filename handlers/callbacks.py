from aiogram.types import CallbackQuery
from aiogram import Router, F
router = Router()


@router.callback_query(F.data == 'love_programming')
async def callback_message(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Я БОЛЬШЕ НЕ МОГУ")

@router.callback_query(F.data == 'favorite_teacher')
async def callback_message(call: CallbackQuery):
    await call.answer()
    await call.message.answer("мой тоже :З")

@router.callback_query(F.data == 'life_without_python')
async def callback_message(call: CallbackQuery):
    await call.answer()
    await call.message.answer("легко и просто")