from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

from src.telegram.filters import allowed_user_filter

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.bot_data.get('is_active', False):
        return await update.message.reply_text("Der Bot ist derzeit inaktiv.")
    
    return await update.message.reply_text("Antwort auf Textnachricht: " + update.message.text)

text_handler = MessageHandler(
    filters=filters.TEXT & (~filters.COMMAND) & allowed_user_filter,
    callback=text
)