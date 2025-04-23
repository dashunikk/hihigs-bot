import pytest
from fixtures import mock_message, mock_router
from handlers.callbacks import callback_message, callback2_message

@pytest.mark.asyncio
async def test_callback_message(mock_message):
    # что-то взяла из фикстур и оно наконец заработало
    # mock_callback_query.message = mock_message

    # Вызов коллбека
    await callback_message(mock_message)

    called_args, called_kwargs = mock_message.message.answer.call_args

    assert called_args[0] == "Я БОЛЬШЕ НЕ МОГУ"

@pytest.mark.asyncio
async def test_callback2_message(mock_message):
    # что-то взяла из фикстур и оно наконец заработало
    # mock_callback_query.message = mock_message

    # Вызов коллбека
    await callback2_message(mock_message)

    called_args, called_kwargs = mock_message.message.answer.call_args

    assert called_args[0] == "мой тоже :З"

    @pytest.mark.asyncio
    async def test_callback2_message(mock_message):
        # что-то взяла из фикстур и оно наконец заработало
        # mock_callback_query.message = mock_message

        # Вызов коллбека
        await callback2_message(mock_message)

        called_args, called_kwargs = mock_message.message.answer.call_args

        assert called_args[0] == "легко и просто"