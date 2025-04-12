from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Antwort auf Textnachricht: " + update.message.text)

text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), text)