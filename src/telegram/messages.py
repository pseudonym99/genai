from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

import filetype
from pydantic_ai import BinaryContent

from src.genai.agent import agent_assistant
from src.telegram.filters import allowed_user_filter

import logging

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get('is_active', False):
        return await update.message.reply_text("Der Bot ist derzeit inaktiv.")
    
    try:
        # create user_prompt
        user_prompt = update.message.text
        
        if "history" not in context.chat_data:
            logging.warning("No history found in chat_data, initializing empty history.")
            context.chat_data['history'] = []

        # run agent
        result = await agent_assistant.run(
            user_prompt=user_prompt,
            message_history=context.chat_data['history'],
        )
        
        reply_text = result.data
        context.chat_data['history'] = result.all_messages()

        return await update.message.reply_text(reply_text)
    except Exception as e:
        logging.error(f"Error in text handler: {e}")
        return await update.message.reply_text("Ein Fehler ist aufgetreten.")


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get('is_active', False):
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
            context.chat_data['history'] = []

        # run agent
        result = await agent_assistant.run(
            user_prompt=user_prompt,
            message_history=context.chat_data['history'],
        )
        
        reply_text = result.data
        context.chat_data['history'] = result.all_messages()

        return await update.message.reply_text(reply_text)
    except Exception as e:
        logging.error(f"Error in image handler: {e}")
        return await update.message.reply_text("Ein Fehler ist aufgetreten.")
    
    

text_handler = MessageHandler(
    filters=filters.TEXT & (~filters.COMMAND) & allowed_user_filter,
    callback=text
)

image_handler = MessageHandler(
    filters=filters.PHOTO & (~filters.COMMAND) & allowed_user_filter,
    callback=image
)