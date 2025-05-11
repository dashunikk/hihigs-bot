import pytest
from main import main
from fixtures import mock_bot, mock_dispatcher, mock_set_commands, mock_router_handlers, mock_router_callbacks, mock_setup_logger


@pytest.mark.asyncio
async def test_main(mock_bot, mock_dispatcher, mock_set_commands, mock_router_handlers, mock_router_callbacks, mock_setup_logger):
    # Вызов функции main
    await main()

    # Проверка
    mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)

    # TODO - техдолг: доделать вызовы функций
    # mock_dispatcher.include_routers.assert_awaited_once_with(mock_router_handlers, mock_router_callbacks)
    # mock_bot.set_commands.assert_awaited_once(mock_bot)
    # mock_setup_logger.assert_awaited_once()