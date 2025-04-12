import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from telegram.ext import ContextTypes

from src.telegram.commands import start, stop


@pytest.fixture
def update():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()
    return update


@pytest.fixture
def context():
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot_data = {}
    context.chat_data = {}
    return context


@pytest.mark.asyncio
async def test_start(update, context):
    await start(update, context)

    assert context.bot_data["is_active"] is True
    assert context.chat_data["history"] == []
    update.message.reply_text.assert_awaited_once_with("Willkommen bei meinem Bot!")


@pytest.mark.asyncio
async def test_stop(update, context):
    await stop(update, context)

    assert context.bot_data["is_active"] is False
    assert context.chat_data["history"] == []
    update.message.reply_text.assert_awaited_once_with("Bot wird gestoppt.")
