from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

import filetype
from pydantic_ai import BinaryContent

from src.genai.assistant import assistant_agent
from src.genai.transcript import transcript_agent

from src.telegram.filters import allowed_user_filter
from src.telegram.helpers import convert_ogg_bytes_to_wav_bytes, escape_markdown_v2

import logging


async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get("is_active", False):
        return await update.message.reply_text("Der Bot ist derzeit inaktiv.")

    try:
        # create user_prompt
        user_prompt = update.message.text

        if "history" not in context.chat_data:
            logging.warning("No history found in chat_data, initializing empty history.")
            context.chat_data["history"] = []

        # run agent
        result = await assistant_agent.run(
            user_prompt=user_prompt,
            message_history=context.chat_data["history"],
        )

        reply_text = result.data
        context.chat_data["history"] = result.all_messages()

        return await update.message.reply_markdown(reply_text)
    except Exception as e:
        logging.error(f"Error in text handler: {e}")
        return await update.message.reply_text("Ein Fehler ist aufgetreten.")


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get("is_active", False):
        return await update.message.reply_text("Der Bot ist derzeit inaktiv.")

    try:
        # create user_prompt
        user_prompt = []

        caption = update.message.caption

        if caption:
            user_prompt.append(caption)

        image = update.message.photo[-1]
        image_file = await context.bot.get_file(image.file_id)
        image_bytes = await image_file.download_as_bytearray()
        kind = filetype.guess(image_bytes)

        if kind is None:
            raise ValueError("Unbekannter Dateityp")

        user_prompt.append(
            BinaryContent(
                data=image_bytes,
                media_type=kind.mime,
            )
        )

        if "history" not in context.chat_data:
            logging.warning("No history found in chat_data, initializing empty history.")
            context.chat_data["history"] = []

        # run agent
        result = await assistant_agent.run(
            user_prompt=user_prompt,
            message_history=context.chat_data["history"],
        )

        reply_text = result.data
        context.chat_data["history"] = result.all_messages()

        return await update.message.reply_text(reply_text)
    except Exception as e:
        logging.error(f"Error in image handler: {e}")
        return await update.message.reply_markdown("Ein Fehler ist aufgetreten.")


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get("is_active", False):
        return await update.message.reply_text("Der Bot ist derzeit inaktiv.")

    try:
        # create transcript
        voice = update.message.voice
        voice_file = await context.bot.get_file(voice.file_id)
        voice_bytes_ogg = await voice_file.download_as_bytearray()
        voice_bytes_wav = convert_ogg_bytes_to_wav_bytes(voice_bytes_ogg)

        binary_content = [
            BinaryContent(
                data=voice_bytes_wav,
                media_type="audio/wav",
            )
        ]
        result = await transcript_agent.run(
            user_prompt=binary_content,
        )
        transcript = escape_markdown_v2(result.data)
        await update.message.reply_markdown_v2(f"_{transcript}_")

        if "history" not in context.chat_data:
            logging.warning("No history found in chat_data, initializing empty history.")
            context.chat_data["history"] = []

        # run agent
        result = await assistant_agent.run(
            user_prompt=transcript,
            message_history=context.chat_data["history"],
        )

        reply_text = result.data
        context.chat_data["history"] = result.all_messages()

        return await update.message.reply_markdown(reply_text)
    except Exception as e:
        logging.error(f"Error in voice handler: {e}")
        return await update.message.reply_text("Ein Fehler ist aufgetreten.")


text_handler = MessageHandler(filters=filters.TEXT & (~filters.COMMAND) & allowed_user_filter, callback=text)

image_handler = MessageHandler(filters=filters.PHOTO & (~filters.COMMAND) & allowed_user_filter, callback=image)

voice_handler = MessageHandler(filters=filters.VOICE & (~filters.COMMAND) & allowed_user_filter, callback=voice)
