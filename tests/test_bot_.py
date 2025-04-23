import pytest
from fixtures import mock_message, mock_router
from handlers.handlers import process_help_command
from aiogram.types import InlineKeyboardMarkup
from handlers.handlers import process_start_command


# Когда тест помечен @pytest.mark.asyncio, он становится сопрограммой (coroutine), вместе с ключевым словом await в теле
# pytest выполнит функцию теста как задачу asyncio, используя цикл событий, предоставляемый фикстурой event_loop
# https://habr.com/ru/companies/otus/articles/337108/

@pytest.mark.asyncio
async def test_process_help_command(mock_router, mock_message):
    # # Вызываем хендлер
    await process_help_command(mock_message)

    # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"

    # Парамаетры, с которыми был вызван хендлер
    called_args, called_kwargs = mock_message.answer.call_args

    # print(called_kwargs)

    # Проверка на корректность текста
    assert called_args[0] == "Помоги!"

    #Вызываем клавиатуру
    markup = called_kwargs["reply_markup"]
    assert isinstance(markup, InlineKeyboardMarkup), "reply_markup не является Inline-клавиатурой"

   # Проверяем, что mock_message был вызван один раз с ожидаемым результатом
   #  mock_message.answer.assert_called_once_with(text="Помоги!...")



@pytest.mark.asyncio
async def test_command_start_handler(mock_router, mock_message):
    """Тест для команды /start"""
    # Вызываем обработчик
    await process_start_command(mock_message)

    # Проверяем, что answer был вызван
    assert mock_message.answer.called, "message.answer не был вызван"

    # Получаем параметры вызова
    called_args, called_kwargs = mock_message.answer.call_args

    # Проверяем, что ответ содержит ID и username пользователя
    response_text = called_kwargs.get("text", "")
    assert str(mock_message.from_user.id) in response_text, "ID пользователя не найден в ответе"
    assert mock_message.from_user.username in response_text, "Username не найден в ответе"