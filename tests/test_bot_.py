import pytest
from fixtures import mock_message, mock_router
from handlers.handlers import process_help_command_handler
from handlers.bot_commands import process_start_command


# Когда тест помечен @pytest.mark.asyncio, он становится сопрограммой (coroutine), вместе с ключевым словом await в теле
# pytest выполнит функцию теста как задачу asyncio, используя цикл событий, предоставляемый фикстурой event_loop
# https://habr.com/ru/companies/otus/articles/337108/


@pytest.mark.asyncio
async def test_command_help_handler(mock_router, mock_message):
    #  Вызываем хендлер
    await process_help_command_handler(mock_message)

    # Проверка, что mock_ был вызван
    assert mock_message.answer.called, "message.answer не был вызван"

    #параметры, с которыми был вызван хендлер
    called_args, called_kwargs = moсk_message.answer.call_args

    assert called_kwargs["test"] == "Помоги!"

    # Проверяем, что mock_ был вызван один раз с ожидаемым результатом
    #mock_message.answer.assert_called_once_with(text="Помоги!")

