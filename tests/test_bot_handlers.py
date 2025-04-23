import pytest
from fixtures import mock_message, mock_router
from handlers.handlers import command_help_handler, command_start_handler


# Когда тест помечен @pytest.mark.asyncio, он становится сопрограммой (coroutine), вместе с ключевым словом await в теле
# pytest выполнит функцию теста как задачу asyncio, используя цикл событий, предоставляемый фикстурой event_loop
# https://habr.com/ru/companies/otus/articles/337108/

@pytest.mark.asyncio
async def test_command_help_handler(mock_router, mock_message):
    # Вызываем хендлер
    await command_help_handler(mock_message)

    # Проверка, что mock_message был вызван
    assert mock_message.answer.called, "message.answer не был вызван"

    # Проверяем, что mock_ был вызван один раз с ожидаемым результатом
    # mock_message.answer.assert_called_once_with(text="Успешно прошел тест")

