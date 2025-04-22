import pytest
from fixtures import mock_callback_query, mock_message
from handlers.callbacks import callback_message

@pytest.mark.asyncio
async def test_callback_message(mock_callback_query, mock_message):
    # что-то взяла из фикстур и оно наконец заработало
    mock_callback_query.message = mock_message

    # Вызов коллбека
    await callback_message(mock_callback_query)

    called_args, called_kwargs = mock_message.answer.call_args

    assert called_args[0] == "Я БОЛЬШЕ НЕ МОГУ"