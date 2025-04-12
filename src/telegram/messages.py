from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

from src.genai.agent import agent_assistant
from src.telegram.filters import allowed_user_filter

import logging

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get('is_active', False):
        return await update.message.reply_text("Der Bot ist derzeit inaktiv.")
    
    try:
        user_prompt = update.message.text

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
    
    

text_handler = MessageHandler(
    filters=filters.TEXT & (~filters.COMMAND) & allowed_user_filter,
    callback=text
)