import pytest
from unittest.mock import AsyncMock, MagicMock


from telegram import Update
from telegram.ext import ContextTypes

from pydantic_ai.models.test import TestModel

from src.telegram.messages import text, image, voice
from src.genai.assistant import agent_assistant


@pytest.mark.asyncio
async def test_text_inactive_bot():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()

    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot_data = {"is_active": False}

    await text(update, context)

    update.message.reply_text.assert_awaited_once_with("Der Bot ist derzeit inaktiv.")


@pytest.mark.asyncio
async def test_text_active_bot():
    update = MagicMock(spec=Update)
    update.message.text = "Hello"
    update.message.reply_text = AsyncMock()

    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot_data = {"is_active": True}
    context.chat_data = {}

    with agent_assistant.override(
        model=TestModel(custom_result_text="Response from agent"),
    ):
        await text(update, context)

    update.message.reply_text.assert_awaited_once_with("Response from agent")


@pytest.mark.asyncio
async def test_image_inactive_bot():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot_data = {"is_active": False}

    await image(update, context)

    update.message.reply_text.assert_awaited_once_with("Der Bot ist derzeit inaktiv.")


@pytest.mark.asyncio
async def test_voice_inactive_bot():
    update = MagicMock(spec=Update)
    update.message.reply_text = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot_data = {"is_active": False}

    await voice(update, context)

    update.message.reply_text.assert_awaited_once_with("Der Bot ist derzeit inaktiv.")
